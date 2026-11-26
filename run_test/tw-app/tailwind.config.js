const { hairlineWidth } = require("nativewind/theme");

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {
      colors: {
        brand: { DEFAULT: "#0c831f", yellow: "#f8cb46", light: "#f1fbf3" },
      },
      borderWidth: { hairline: hairlineWidth() },
    },
  },
  plugins: [],
};
