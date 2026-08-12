const { isPrimary } = require('node:cluster');

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // tous tes composants React
  ],
  theme: {
    extend: {
      colors: {
        Primary:{
        50: '#eff6ff',
        100: '#dbeafe',
        900: '#1e3a8a',
        },
        // Couleurs principales
        accent: "#aa3bff",
        "accent-light": "rgba(170, 59, 255, 0.1)",
        "accent-dark": "#8a2bcc",
        bg: "#ffffff",
        "bg-dark": "#08060d",
        text: "#6b6375",
        "text-dark": "#08060d",
        border: "#e5e4e7",
        error: "#ff4d4f",
        success: "#52c41a",
        warning: "#faad14",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui"],
        mono: ["ui-monospace", "SFMono-Regular"],
      },
      borderRadius: {
        "2xl": "1rem",
      },
      boxShadow: {
        soft: "0 4px 6px rgba(0,0,0,0.05)",
        medium: "0 8px 12px rgba(0,0,0,0.1)",
      },
      keyframes: {
        modalEnter: {
          "0%": { opacity: 0, transform: "scale(0.95)" },
          "100%": { opacity: 1, transform: "scale(1)" },
        },
        modalExit: {
          "0%": { opacity: 1, transform: "scale(1)" },
          "100%": { opacity: 0, transform: "scale(0.95)" },
        },
      },
      animation: {
        "modal-enter": "modalEnter 0.3s ease-out forwards",
        "modal-exit": "modalExit 0.2s ease-in forwards",
      },
    },
  },
  plugins: [],
};