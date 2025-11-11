// Theme toggle functionality for SheetAlchemy documentation

(function() {
    // Check for saved theme preference or default to dark
    const getPreferredTheme = () => {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            return savedTheme;
        }
        // Default to dark theme
        return 'dark';
    };

    // Apply theme
    const setTheme = (theme) => {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        updateToggleButton(theme);
    };

    // Update toggle button icon
    const updateToggleButton = (theme) => {
        const button = document.getElementById('theme-toggle');
        if (button) {
            button.innerHTML = theme === 'dark' ? '☀️' : '🌙';
            button.setAttribute('aria-label', theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode');
        }
    };

    // Toggle theme
    const toggleTheme = () => {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
    };

    // Initialize theme when DOM is ready
    const initTheme = () => {
        const theme = getPreferredTheme();
        setTheme(theme);

        // Create toggle button
        const button = document.createElement('button');
        button.id = 'theme-toggle';
        button.className = 'theme-toggle';
        button.setAttribute('aria-label', 'Toggle theme');
        button.onclick = toggleTheme;
        document.body.appendChild(button);

        updateToggleButton(theme);
    };

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTheme);
    } else {
        initTheme();
    }

    // Listen for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            setTheme(e.matches ? 'dark' : 'light');
        }
    });
})();
