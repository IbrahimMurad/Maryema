/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./public/**/*.html", "./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        roboto: ["Roboto", "sans-serif"],
        autour: ['"Autour One"', "sans-serif"],
        charm: ['"Charm"', "sans-serif"],
        cookie: ['"Cookie"', "sans-serif"],
        kalam: ['"Kalam"', "sans-serif"],
        lato: ['"Lato"', "sans-serif"],
        londrina: ['"Londrina Solid"', "sans-serif"],
        notoSerif: ['"Noto Serif"', "serif"],
        paprika: ['"Paprika"', "sans-serif"],
        sourGummy: ['"Sour Gummy"', "sans-serif"],
        alegreya: ["Alegreya", "sans-serif"],
        lusitana: ["Lusitana", "sans-serif"],
      },
    },
  },
  plugins: [require("@tailwindcss/forms")],
};
