/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./src/**/*.{js,jsx,ts,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#2E8B57', // Amypo Green
                    hover: '#256f46',
                },
                bg: {
                    primary: '#ffffff',
                    secondary: '#f8fafc',
                    tertiary: '#f1f5f9',
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
            }
        },
    },
    plugins: [],
}
