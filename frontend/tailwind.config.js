/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#557C78',
          hover: '#456864',
          dark: '#385451',
          light: '#6E9490',
        },
        secondary: {
          DEFAULT: '#A9C4B8',
          hover: '#98B5A9',
          light: '#C4D8CF',
        },
        background: '#F7F9F7',
        surface: '#FFFFFF',
        textMain: '#253532',
        textMuted: '#5C716D',
        accent: {
          DEFAULT: '#DCEAE3',
          border: '#C2D9CE',
          soft: '#EAF3EF',
        },
        crisis: {
          red: '#D9534F',
          bg: '#FFF2F2',
          border: '#F5C6CB',
          text: '#721C24'
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      boxShadow: {
        'soft': '0 4px 20px -2px rgba(85, 124, 120, 0.08)',
        'card': '0 2px 10px rgba(37, 53, 50, 0.04)',
      }
    },
  },
  plugins: [],
}

