module.exports = {
    content: [
      "./src/**/*.{html,js,vue}",
    ],
    theme: {
        extend: {
            colors: {
                quaternary: "var(--quaternary)",
                "quaternary-focus": "var(--quaternary-focus)",
                "quaternary-content": "var(--quaternary-content)",
                tertiary: "var(--tertiary)",
                "tertiary-focus": "var(--tertiary-focus)",
                "tertiary-content": "var(--tertiary-content)",
                quinternary: "var(--quinternary)",
                "quinternary-focus": "var(--quinternary-focus)",
                "quinternary-content": "var(--quinternary-content)",
            },
        },
    },
    plugins: [require("daisyui")],
    darkMode: 'class',
    daisyui: {
        themes: [ {
                'my-dark': {
                    'primary' : '#376a2f',
                    'primary-focus' : '#55a548',
                    'primary-content' : '#ffffff',

                    'secondary' : '#0a1172',
                    'secondary-focus' : '#3944bc',
                    'secondary-content' : '#ffffff',

                    'accent' : '#daa520',
                    'accent-focus' : '#ffd700',
                    'accent-content' : '#000000',

                    '--tertiary': '#e11584',
                    '--tertiary-focus': '#f699cd',
                    '--tertiary-content': '#000000',

                    '--quaternary': '#610c04',
                    '--quaternary-focus': '#d21404',
                    '--quaternary-content': '#ffffff',

                    '--quinternary': '#d16002',
                    '--quinternary-focus': '#fcae1e',
                    '--quinternary-content': '#ffffff',

                    'neutral' : '#2a2a37',
                    'neutral-focus' : '#16181d',
                    'neutral-content' : '#ffffff',

                    'base-100' : '#282c34',
                    'base-200' : '#1f2228',
                    'base-300' : '#16181d',
                    'base-content' : '#ebecf0',

                    'info' : '#38b6ff',
                    'success' : '#7bc828',
                    'warning' : '#dbac48',
                    'error' : '#ff4d4d',

                    '--rounded-box': '1.5rem',
                    '--rounded-btn': '1.5rem',
                    '--rounded-badge': '1.5rem',

                    '--animation-btn': '.25s',
                    '--animation-input': '.2s',

                    '--btn-text-case': 'uppercase',
                    '--navbar-padding': '.5rem',
                    '--border-btn': '1.5px',
                },
            },
        ],
        darkTheme: 'my-dark',
        base: true,
        styled: true,
        prefix: "",
        logs: true,
        themeRoot: ":root",
    }
  };
  