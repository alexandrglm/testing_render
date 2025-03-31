

document.addEventListener('DOMContentLoaded', function() {



    // 0 -  ACE's
    
    // editor ace
    const editor = ace.edit("markdown-editor");
    editor.setTheme("ace/theme/chrome");
    editor.session.setMode("ace/mode/markdown");
    editor.setOptions({ 
        fontSize: "14px", 
        showPrintMargin: false, 
        wrap: true 
    });

    // filters' regex ace
    const exclusionEditor = ace.edit("exclusionEditor");
    exclusionEditor.setTheme("ace/theme/chrome");
    exclusionEditor.session.setMode("ace/mode/text");
    exclusionEditor.setOptions({
        fontSize: "14px",
        showPrintMargin: false,
        wrap: true
    });

    const state = {
        currentFilters: {
            exclusionPatterns: [],
            elementMappings: {}
        },
        currentTemplate: 'default',
        currentFile: null,
        currentMode: 'basic'
    };




    const filtersButton = document.querySelector("[data-bs-target='#filtersCollapse']");
    const basicModeRadio = document.getElementById('basicMode');
    const advancedModeRadio = document.getElementById('advancedMode');
    const regexPreview = document.getElementById('regexPreview');
    const regexError = document.getElementById('regexError');
    const modeHelp = document.getElementById('modeHelp');
    const scrapeBtn = document.getElementById('scrape-btn');
    const saveBtn = document.getElementById('save-btn');
    const templateSelect = document.getElementById('templateSelect');
    const addMappingBtn = document.getElementById('addMappingBtn');
    const saveTemplateBtn = document.getElementById('saveTemplateBtn');


    loadFilters();
    loadTemplates();
    updateUI();


    if (filtersButton) filtersButton.addEventListener('click', filtersButtonToggler);
    if (scrapeBtn) scrapeBtn.addEventListener('click', scrapePage);
    if (saveBtn) saveBtn.addEventListener('click', downloadMarkdown);
    if (templateSelect) templateSelect.addEventListener('change', loadTemplate);
    if (addMappingBtn) addMappingBtn.addEventListener('click', addMapping);
    if (saveTemplateBtn) saveTemplateBtn.addEventListener('click', saveTemplate);


    function filtersButtonToggler() {
        setTimeout(() => {
            if (document.querySelector("#filtersCollapse").classList.contains("show")) {
                console.log('DEBUG: CLOSED')
            } else {
                console.log('DEBUG: OPEN')
            }
        }, 300);
    };



    /////////////////////////////////////////////////////////////////////////////////////
    // 1.1 . EXCLUSIONS
    basicModeRadio.addEventListener('change', function() {
        if (this.checked) {
            switchToBasicMode();
        }
    });

    advancedModeRadio.addEventListener('change', function() {
        if (this.checked) {
            switchToAdvancedMode();
        }
    });

    exclusionEditor.session.on('change', function() {
        updateRegexPreview();
    });
    function switchToBasicMode() {
        state.currentMode = 'basic';
        exclusionEditor.session.setMode("ace/mode/text");
        modeHelp.textContent = "BASIC mode: Paste raw text to exclude.";
        updateRegexPreview();
    }


    function switchToAdvancedMode() {
        state.currentMode = 'advanced';
        exclusionEditor.session.setMode("ace/mode/javascript");
        modeHelp.textContent = "ADVANCED mode: Write REGEX patterns directly. Validate with CTRL+Enter.";
        updateRegexPreview();
    }

    function updateRegexPreview() {

        const content = exclusionEditor.getValue();
        regexError.style.display = 'none';

        if (state.currentMode === 'basic') {
        
            if (content.trim() === '') {
                regexPreview.textContent = '';
                return;
            }
        
            regexPreview.textContent = convertToRegex(content);
        
        } else {
            regexPreview.textContent = content;
            validateRegex(content);
        }
    }


    function convertToRegex(text) {
        return text
            .replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
            .replace(/\\\*/g, '.*?')
            .replace(/\n/g, '\\n');
    }


    function validateRegex(pattern) {
        
        try {
            new RegExp(pattern);
            regexPreview.classList.remove('invalid');
            return true;
        } catch (e) {
            regexPreview.classList.add('invalid');
            regexError.style.display = 'block';
            return false;
        }
    }

    function addExclusion() {
        
        const patternText = exclusionEditor.getValue().trim();
        
        if (!patternText) {
            showStatus('Enter an exclusion pattern', 'error');
            return;
        }

        const pattern = {
            raw: patternText,
            is_regex: state.currentMode === 'advanced',
            lines: state.currentMode === 'basic' ? patternText.split('\n') : undefined
        };

        if (state.currentMode === 'advanced' && !validateRegex(patternText)) {
            showStatus('Invalid regex pattern', 'error');
            return;
        }

        if (isDuplicatePattern(pattern)) {
            showStatus('The pattern already exists!', 'warning');
            return;
        }

        state.currentFilters.exclusionPatterns.push(pattern);
        saveFilters();
        updateUI();
        showStatus('Added exclusion pattern', 'success');
        exclusionEditor.setValue('');
    }


    function isDuplicatePattern(pattern) {
        return state.currentFilters.exclusionPatterns.some(
            p => p.raw === pattern.raw && p.is_regex === pattern.is_regex
        );
    }


    function removeExclusion(index) {
        if (index >= 0 && index < state.currentFilters.exclusionPatterns.length) {
            state.currentFilters.exclusionPatterns.splice(index, 1);
            saveFilters();
            updateUI();
            showStatus('Pattern removed', 'info');
        }
    }


    function clearExclusions() {
        state.currentFilters.exclusionPatterns = [];
        saveFilters();
        updateUI();
        showStatus('Exclusions cleared', 'info');
    }

    /////////////////////////////////////////////////////////////////////////////////////
    // 1.2  MAPPERS
    function addMapping() {
        const selector = document.getElementById('elementSelector').value.trim();
        const type = document.getElementById('elementType').value;
        
        if (!selector || !type) {
            showStatus('Complete both fields', 'error');
            return;
        }

        if (state.currentFilters.elementMappings[selector]) {
            showStatus('This selector is already mapped', 'warning');
            return;
        }

        state.currentFilters.elementMappings[selector] = type;
        saveFilters();
        updateUI();
        showStatus(`Mapping added: ${selector} → ${type}`, 'success');
        document.getElementById('elementSelector').value = '';
    }


    function removeMapping(selector) {
        if (state.currentFilters.elementMappings[selector]) {
            delete state.currentFilters.elementMappings[selector];
            saveFilters();
            updateUI();
            showStatus(`Mapping removed: ${selector}`, 'info');
        }
    }


    function clearMappings() {
        state.currentFilters.elementMappings = {};
        saveFilters();
        updateUI();
        showStatus('Mappings cleared', 'info');
    }

    /////////////////////////////////////////////////////////////////////////////////////
    // 1.3 
    function updateUI() {
        updateExclusionList();
        updateMappingList();
    }
    /////////////////////////////////////////////////////////////////////////////////////
    // 1.3  EXCLUSSIONS
    function updateExclusionList() {
        const exclusionList = document.getElementById('exclusionList');
        if (!exclusionList) return;

        exclusionList.innerHTML = '';
        state.currentFilters.exclusionPatterns.forEach((pattern, index) => {
            const item = document.createElement('div');
            item.className = 'filter-item';
            
            const badge = document.createElement('span');
            badge.className = 'badge ' + (pattern.is_regex ? 'bg-warning' : 'bg-success');
            badge.textContent = pattern.is_regex ? 'ADV' : 'BASIC';
            
            const content = document.createElement('span');
            content.style.marginLeft = '8px';
            content.textContent = pattern.raw.length > 50 
                ? pattern.raw.substring(0, 50) + '...' 
                : pattern.raw;
            
            const btn = document.createElement('button');
            btn.className = 'btn btn-sm btn-danger ms-auto';
            btn.innerHTML = '<i class="bi bi-trash"></i>';
            btn.onclick = () => removeExclusion(index);
            
            item.appendChild(badge);
            item.appendChild(content);
            item.appendChild(btn);
            
            exclusionList.appendChild(item);
        });
    }
    /////////////////////////////////////////////////////////////////////////////////////
    // 1.3 MAPPERS
    function updateMappingList() {
        const mappingList = document.getElementById('mappingList');
        if (!mappingList) return;

        mappingList.innerHTML = '';
        Object.entries(state.currentFilters.elementMappings).forEach(([selector, type]) => {
            const item = document.createElement('div');
            item.className = 'filter-item';
            item.innerHTML = `
                <span>${escapeHtml(selector)} → ${escapeHtml(type)}</span>
                <button class="btn btn-sm btn-danger" onclick="removeMapping('${escapeHtml(selector).replace(/'/g, "\\'")}')">
                    <i class="bi bi-trash"></i>
                </button>
            `;
            mappingList.appendChild(item);
        });
    }

    /////////////////////////////////////////////////////////////////////////////////////
    // 1.4  RULESETS Handler
    function loadFilters() {
        try {
            const savedFilters = localStorage.getItem('scraperFilters');
            if (savedFilters) {
                const parsed = JSON.parse(savedFilters);
                state.currentFilters = {
                    exclusionPatterns: Array.isArray(parsed.exclusionPatterns) ? 
                        parsed.exclusionPatterns.map(p => ({
                            ...p,
                            // Mantener compatibilidad con versiones anteriores
                            is_regex: p.is_regex || false
                        })) : [],
                    elementMappings: parsed.elementMappings && typeof parsed.elementMappings === 'object' ? 
                        parsed.elementMappings : {}
                };
            }
        } catch (e) {
            console.error("Error parsing saved filters:", e);
            localStorage.removeItem('scraperFilters');
        }
    }

    function saveFilters() {
        localStorage.setItem('scraperFilters', JSON.stringify({
            exclusionPatterns: state.currentFilters.exclusionPatterns,
            elementMappings: state.currentFilters.elementMappings
        }));
    }

    async function loadTemplates() {
        try {
            const response = await fetch('/13/filtersmappers/');
            if (!response.ok) {
                throw new Error('Failed to load templates');
            }
            
            const data = await response.json();
            const templates = data.templates || [];
            const select = document.getElementById('templateSelect');
            
            if (select) {
                select.innerHTML = '<option value="">Select filter ruleset...</option>';
                templates.forEach(template => {
                    const option = document.createElement('option');
                    option.value = template;
                    option.textContent = template;
                    select.appendChild(option);
                });

                if (state.currentTemplate) {
                    select.value = state.currentTemplate;
                }
            }
        } catch (error) {
            console.error('Error loading templates:', error);
            showStatus(`Error loading templates: ${error.message}`, 'error');
        }
    }

    async function loadTemplate() {
        const templateName = templateSelect?.value;
        if (!templateName) return;

        try {
            const response = await fetch(`/13/mapper/${templateName}`);
            if (!response.ok) {
                throw new Error('Failed to load ruleset');
            }
            
            const template = await response.json();
            
            state.currentFilters = {
                exclusionPatterns: template.exclusion_patterns || [],
                elementMappings: template.element_mappings || {}
            };

            state.currentTemplate = templateName;
            saveFilters();
            updateUI();
            showStatus(`Template "${templateName}" loaded`, 'success');
        } catch (error) {
            console.error('Error loading template:', error);
            showStatus(`Error loading template: ${error.message}`, 'error');
        }
    }

    async function saveTemplate() {
        const templateName = document.getElementById('templateName')?.value.trim();
        const templateDesc = document.getElementById('templateDescription')?.value.trim() || '';
        
        if (!templateName) {
            showStatus('Template name is required', 'error');
            return;
        }

        try {
            const response = await fetch('/13/save-template', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    name: templateName,
                    description: templateDesc,
                    filters: {
                        elementMappings: state.currentFilters.elementMappings,
                        exclusionPatterns: state.currentFilters.exclusionPatterns.map(p => ({
                            raw: p.raw,
                            is_regex: p.is_regex,
                            lines: p.is_regex ? undefined : p.raw.split('\n')
                        }))
                    }
                })
            });
            
            if (!response.ok) {
                throw new Error('Failed to save template');
            }
            
            showStatus(`Template "${templateName}" saved successfully`, 'success');
            document.getElementById('templateName').value = '';
            document.getElementById('templateDescription').value = '';
            await loadTemplates();
        } catch (error) {
            console.error('Error saving template:', error);
            showStatus(`Error: ${error.message}`, 'error');
        }
    }

    /////////////////////////////////////////////////////////////////////////////////////
    // 2. URI SCRAPPY
    async function scrapePage() {

        const url = document.getElementById('targetUrl')?.value.trim();
        const scroll = document.getElementById('scrollCheck')?.checked || false;
        const waitForElement = document.getElementById('waitForElement')?.value.trim() || '';
        
        if (!url) {
            showStatus('Please, provide a valid URL', 'error');
            return;
        }
    
        try {
            showStatus('Processing...', 'info');
            
            const response = await fetch('/13/scrappy', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    url: url,
                    options: {
                        scroll: scroll,
                        wait_for_element: waitForElement || null
                    },
                    filters: {
                        elementMappings: state.currentFilters.elementMappings,
                        exclusionPatterns: state.currentFilters.exclusionPatterns.map(p => ({
                            raw: p.raw,
                            is_regex: p.is_regex
                        }))
                    },
                    template: state.currentTemplate
                })
            });
            
            if (!response.ok) {
                throw new Error('Scraping failed');
            }
    
            const result = await response.json();
            
            editor.setValue(result.markdown || result.content || '', -1);
            state.currentFile = result.filename || 'scraped_content.md';
            
            const metadataDisplay = document.getElementById('metadata-display');
            
            if (metadataDisplay && result.metadata) {
                metadataDisplay.innerHTML = `
                    <p><strong>Title:</strong> ${escapeHtml(result.metadata.title || 'N/A')}</p>
                    <p><strong>URL:</strong> <a href="${escapeHtml(result.metadata.url || '#')}" target="_blank">${escapeHtml(result.metadata.url || 'N/A')}</a></p>
                    <p><strong>Timestamp:</strong> ${result.metadata.timestamp ? new Date(result.metadata.timestamp).toLocaleString() : 'N/A'}</p>
                `;
            }
            
            showStatus('Scraping completed', 'success');
        
        } catch (error) {
        
            console.error("Error scraping:", error);
        
            showStatus(`Error: ${error.message}`, 'error');
        
            editor.setValue('');
        
            const metadataDisplay = document.getElementById('metadata-display');
        
            if (metadataDisplay) metadataDisplay.innerHTML = '';
        }
    }

    /////////////////////////////////////////////////////////////////////////////////////
    // md dowbn
    function downloadMarkdown() {

        const content = editor.getValue();
        
        if (!content) {
            showStatus('Empty md file won\'t be downloaded', 'error');
            return;
        }

        try {
        
            const blob = new Blob([content], { type: 'text/markdown' });
        
            const url = URL.createObjectURL(blob);
        
            const a = document.createElement('a');
        
            a.href = url;
        
            a.download = state.currentFile || 'scraped_content.md';
        
            document.body.appendChild(a);
        
            a.click();
            document.body.removeChild(a);
        
            setTimeout(() => URL.revokeObjectURL(url), 100);
        
        } catch (error) {
        
            console.error('Error downloading markdown:', error);
            showStatus(`Download error: ${error.message}`, 'error');
        
        }
    }

    /////////////////////////////////////////////////////////////////////////////////////
    // 3. Debuggings
    function showStatus(message, type = 'info') {
        const statusElement = document.getElementById('statusMessage');
        if (!statusElement) return;
        
        statusElement.textContent = message;
        statusElement.style.display = 'block';
        statusElement.className = 'alert';
        
        const typeClasses = {
            'error': 'alert-danger',
            'success': 'alert-success',
            'warning': 'alert-warning',
            'info': 'alert-info'
        };
        
        statusElement.classList.add(typeClasses[type] || 'alert-info');
        
        setTimeout(() => {
            statusElement.style.display = 'none';
        }, 5000);
    }

    // OThers
    function escapeHtml(unsafe) {
        if (!unsafe) return '';
        return unsafe.toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    
    /////////////////////////////////////////////////////////////////////////////////////
    window.filtersButton = filtersButtonToggler;
    window.addExclusion = addExclusion;
    window.removeExclusion = removeExclusion;
    window.clearExclusions = clearExclusions;
    window.addMapping = addMapping;
    window.removeMapping = removeMapping;
    window.clearMappings = clearMappings;
    window.saveTemplate = saveTemplate;
    window.loadTemplate = loadTemplate;
    window.scrapePage = scrapePage;
    window.downloadMarkdown = downloadMarkdown;
});

