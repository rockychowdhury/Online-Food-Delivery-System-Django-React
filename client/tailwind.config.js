/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Custom Colors
      colors: {
        primary: {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f97316', // Main Orange
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
          950: '#431407',
        },
        secondary: {
          50: '#f0fdf4',
          100: '#dcfce7',
          200: '#bbf7d0',
          300: '#86efac',
          400: '#4ade80',
          500: '#22c55e', // Fresh Green
          600: '#16a34a',
          700: '#15803d',
          800: '#166534',
          900: '#14532d',
          950: '#052e16',
        },
        accent: {
          50: '#fefce8',
          100: '#fef9c3',
          200: '#fef08a',
          300: '#fde047',
          400: '#facc15', // Golden Yellow
          500: '#eab308',
          600: '#ca8a04',
          700: '#a16207',
          800: '#854d0e',
          900: '#713f12',
          950: '#422006',
        },
        // Food Category Colors
        food: {
          pizza: '#e53e3e',
          burger: '#d69e2e',
          asian: '#38a169',
          dessert: '#d53f8c',
          healthy: '#4299e1',
          coffee: '#a0522d',
        },
        // Status Colors
        success: '#22c55e',
        warning: '#f59e0b',
        error: '#ef4444',
        info: '#3b82f6',
      },

      // Custom Font Families
      fontFamily: {
        primary: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        secondary: ['Poppins', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        accent: ['Outfit', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },

      // Custom Font Sizes
      fontSize: {
        'hero': ['4.5rem', { lineHeight: '1.1' }],
        '5xl': ['3rem', { lineHeight: '1.2' }],
        '4xl': ['2.25rem', { lineHeight: '1.25' }],
        '3xl': ['1.875rem', { lineHeight: '1.3' }],
        '2xl': ['1.5rem', { lineHeight: '1.35' }],
        'xl': ['1.25rem', { lineHeight: '1.4' }],
        'lg': ['1.125rem', { lineHeight: '1.5' }],
        'base': ['1rem', { lineHeight: '1.6' }],
        'sm': ['0.875rem', { lineHeight: '1.5' }],
        'xs': ['0.75rem', { lineHeight: '1.4' }],
      },

      // Custom Spacing
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },

      // Custom Border Radius
      borderRadius: {
        'xl': '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      },

      // Custom Box Shadows
      boxShadow: {
        'food-card': '0 4px 20px rgba(0, 0, 0, 0.08)',
        'floating': '0 8px 32px rgba(0, 0, 0, 0.12)',
        'soft': '0 2px 15px rgba(0, 0, 0, 0.08)',
        'medium': '0 4px 25px rgba(0, 0, 0, 0.1)',
        'strong': '0 8px 40px rgba(0, 0, 0, 0.15)',
      },

      // Custom Breakpoints
      screens: {
        'xs': '475px',
        '3xl': '1920px',
      },

      // Custom Grid Templates
      gridTemplateColumns: {
        'auto-fit-xs': 'repeat(auto-fit, minmax(200px, 1fr))',
        'auto-fit-sm': 'repeat(auto-fit, minmax(250px, 1fr))',
        'auto-fit-md': 'repeat(auto-fit, minmax(300px, 1fr))',
        'auto-fit-lg': 'repeat(auto-fit, minmax(350px, 1fr))',
      },

      // Custom Aspect Ratios
      aspectRatio: {
        'food-card': '4 / 3',
        'hero': '16 / 9',
      },

      // Custom Backdrop Blur
      backdropBlur: {
        'xs': '2px',
      },

      // Custom Z-Index
      zIndex: {
        'dropdown': '1000',
        'sticky': '1010',
        'overlay': '1020',
        'modal': '1030',
        'popover': '1040',
        'tooltip': '1050',
        'toast': '1060',
      },

      // Custom Transitions
      transitionDuration: {
        '400': '400ms',
        '600': '600ms',
      },

      // Custom Transform
      scale: {
        '102': '1.02',
        '103': '1.03',
      },
    },
  },
  plugins: [],
}

