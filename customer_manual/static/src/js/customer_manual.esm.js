/** @odoo-module **/

import { Component, markup, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class CustomerManual extends Component {
    setup() {

        this.user = useService("user");
        this.state = useState({
            canSeeButton: false, // Initial button visibility state
        });

        // Check if the user belongs to the "customer_manual.group_customer_manual_edit" group
        onWillStart(async () => {
            this.state.canSeeButton = await this.user.hasGroup("customer_manual.group_customer_manual_edit");

        });
        this.orm = useService("orm");
        this.notification = useService("notification");

        // CKEditor instances are external objects, so they are kept outside OWL state.
        this.noteEditors = {};

        this.state = useState({
            loading: true,
            saving: false,
            data: null,
            selectedSectionKey: null,
            searchText: "",
            editingNotes: false,
            showTechnicalDetails: false,
            openModuleKeys: {},
        });

        // Arrow functions keep `this` bound when handlers are called from the template.
        this.selectSection = async (section) => {
            await this.destroyEditors();

            this.state.selectedSectionKey = section.key;
            this.state.editingNotes = false;
            this.state.showTechnicalDetails = false;
            this.state.openModuleKeys = {};
        };

        this.onSearchInput = (ev) => {
            this.state.searchText = ev.target.value || "";
            this.ensureSelectedSectionIsVisible();
        };

        this.clearSearch = () => {
            this.state.searchText = "";
            this.ensureSelectedSectionIsVisible();
        };

        this.enterEditMode = async () => {
            this.state.editingNotes = true;
            await this.initEditors();
        };

        this.addNote = async () => {
            if (!this.selectedSection) {
                return;
            }

            this.selectedSection.notes.push({
                id: `new_${Date.now()}`,
                title: "",
                body_html: "<p></p>",
                sequence: (this.selectedSection.notes.length + 1) * 10,
            });

            this.state.editingNotes = true;
            await this.initEditors();
        };

        this.removeNote = async (note) => {
            await this.destroyEditor(note.id);

            if (!this.selectedSection) {
                return;
            }

            this.selectedSection.notes = this.selectedSection.notes.filter(
                (item) => item.id !== note.id
            );
        };

        this.cancelEditNotes = async () => {
            this.state.editingNotes = false;
            await this.destroyEditors();
            await this.load(false);
        };

        this.saveNotes = async () => {
            if (!this.selectedSection || this.state.saving) {
                return;
            }

            this.state.saving = true;

            try {
                this.syncEditorsToNotes();

                await this.orm.call(
                    "customer.manual.service",
                    "save_section_notes",
                    [
                        this.selectedSection.key,
                        this.selectedSection.name,
                        this.selectedSection.notes,
                    ]
                );

                this.notification.add("Ohje tallennettu.", { type: "success" });

                this.state.editingNotes = false;
                await this.destroyEditors();
                await this.load(false);
            } finally {
                this.state.saving = false;
            }
        };

        this.toggleTechnicalDetails = () => {
            this.state.showTechnicalDetails = !this.state.showTechnicalDetails;
        };

        this.toggleModule = (module) => {
            this.state.openModuleKeys[module.key] = !this.state.openModuleKeys[module.key];
        };

        onWillStart(() => this.load(true));
    }

    async load(showLoading = true) {
        if (showLoading) {
            this.state.loading = true;
        }

        await this.destroyEditors();

        this.state.data = await this.orm.call(
            "customer.manual.service",
            "get_data",
            [],
            {}
        );

        this.ensureSelectedSectionIsVisible();

        if (showLoading) {
            this.state.loading = false;
        }
    }

    async initEditors() {
        await this.waitForDomRender();

        if (!window.ClassicEditor) {
            this.notification.add("CKEditor ei latautunut. Tarkista moduulin assetit.", {
                type: "danger",
            });
            return;
        }

        const textareas = document.querySelectorAll(
            ".o_customer_manual textarea.cm-ckeditor"
        );

        for (const textarea of textareas) {
            const noteId = textarea.dataset.noteId;

            if (!noteId || this.noteEditors[noteId]) {
                continue;
            }

            textarea.value = textarea.dataset.initialValue || "";

            try {
                this.noteEditors[noteId] = await window.ClassicEditor.create(textarea, {
                    toolbar: [
                        "heading",
                        "|",
                        "bold",
                        "italic",
                        "link",
                        "bulletedList",
                        "numberedList",
                        "blockQuote",
                        "|",
                        "undo",
                        "redo",
                    ],
                });
            } catch (error) {
                console.error("CKEditor initialization failed:", error);
                this.notification.add("Editorin alustus epäonnistui.", {
                    type: "danger",
                });
            }
        }
    }

    async waitForDomRender() {
        // Textareas are added by OWL only after edit mode has been rendered.
        await new Promise((resolve) => requestAnimationFrame(resolve));
        await new Promise((resolve) => requestAnimationFrame(resolve));
    }

    syncEditorsToNotes() {
        // CKEditor keeps the live HTML internally. Copy it back before saving.
        for (const note of this.selectedSection.notes) {
            const editor = this.noteEditors[String(note.id)];
            if (editor) {
                note.body_html = editor.getData() || "";
            }
        }
    }

    async destroyEditor(noteId) {
        const key = String(noteId);
        const editor = this.noteEditors[key];

        if (!editor) {
            return;
        }

        try {
            await editor.destroy();
        } catch (error) {
            console.warn("CKEditor destroy failed:", error);
        }

        delete this.noteEditors[key];
    }

    async destroyEditors() {
        for (const key of Object.keys(this.noteEditors)) {
            await this.destroyEditor(key);
        }

        this.noteEditors = {};
    }

    isModuleOpen(module) {
        return Boolean(this.state.openModuleKeys[module.key]);
    }

    getHtml(value) {
        // Render stored HTML as HTML, not as escaped text.
        return markup(value || "");
    }

    get filteredSections() {
        const sections = this.state.data?.sections || [];
        const searchText = (this.state.searchText || "").trim().toLowerCase();

        if (!searchText) {
            return sections;
        }

        return sections.filter((section) => {
            const sectionMatch = (section.name || "").toLowerCase().includes(searchText);

            const noteMatch = (section.notes || []).some((note) => {
                return (
                    (note.title || "").toLowerCase().includes(searchText) ||
                    (note.body_html || "").toLowerCase().includes(searchText)
                );
            });

            const moduleMatch = (section.modules || []).some((module) => {
                return (
                    (module.name || "").toLowerCase().includes(searchText) ||
                    (module.technical_name || "").toLowerCase().includes(searchText)
                );
            });

            return sectionMatch || noteMatch || moduleMatch;
        });
    }

    get selectedSection() {
        return (
            (this.state.data?.sections || []).find(
                (section) => section.key === this.state.selectedSectionKey
            ) || null
        );
    }

    get visibleSelectedModules() {
        const section = this.selectedSection;

        if (!section) {
            return [];
        }

        const searchText = (this.state.searchText || "").trim().toLowerCase();

        if (!searchText) {
            return section.modules || [];
        }

        return (section.modules || []).filter((module) => {
            return (
                (section.name || "").toLowerCase().includes(searchText) ||
                (module.name || "").toLowerCase().includes(searchText) ||
                (module.technical_name || "").toLowerCase().includes(searchText)
            );
        });
    }

    get technicalModules() {
        return this.visibleSelectedModules.map((module) => ({
            ...module,
            description: markup(module.description_html || ""),
        }));
    }

    get hasSearch() {
        return Boolean((this.state.searchText || "").trim());
    }

    get hasNotes() {
        return Boolean(this.selectedSection?.notes?.length);
    }

    get isEmpty() {
        return !this.filteredSections.length;
    }

    ensureSelectedSectionIsVisible() {
        const sections = this.filteredSections;
        const selectedVisible = sections.some(
            (section) => section.key === this.state.selectedSectionKey
        );

        if (!selectedVisible) {
            this.state.selectedSectionKey = sections[0]?.key || null;
        }

        if (!this.state.selectedSectionKey && sections.length) {
            this.state.selectedSectionKey = sections[0].key;
        }
    }
}

CustomerManual.template = "customer_manual.CustomerManual";

registry.category("actions").add("customer_manual.open", CustomerManual);