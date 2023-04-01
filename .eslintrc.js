const svelte3RulesToExclude = [
    'a11y-click-events-have-key-events'
]

module.exports = {
    parser: '@typescript-eslint/parser',
    root: true,
    extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'plugin:@typescript-eslint/recommended-requiring-type-checking'
    ],
    parserOptions: {
        project: 'tsconfig.json',
        sourceType: 'module',
        ecmaVersion: 2022, // latest version
        tsconfigRootDir: __dirname,
        extraFileExtensions: ['.svelte']
    },
    env: {
        es6: true,
        browser: true
    },
    overrides: [
        {
            files: ['**/*.svelte'],
            processor: 'svelte3/svelte3',
            rules: {
                // suppress errors on $store usage
                '@typescript-eslint/no-unsafe-argument': 'off',
                '@typescript-eslint/no-unsafe-assignment': 'off',
                '@typescript-eslint/no-unsafe-call': 'off',
                '@typescript-eslint/no-unsafe-member-access': 'off'
            }
        }
    ],
    settings: {
        'svelte3/typescript': require('typescript'),
        'svelte3/ignore-warnings': w => svelte3RulesToExclude.includes(w.code)
    },
    plugins: [
        'svelte3',
        '@typescript-eslint',
        'eslint-plugin-tsdoc'
    ],
    ignorePatterns: [
        '.eslintrc.js',
        'webpack.config.js',
        'node_modules'
    ],
    rules: {
        // only single quotes
        quotes: ['error', 'single'],
        // no semicolons
        semi: ['error', 'never'],
        // warn on wrong doc syntax
        'tsdoc/syntax': 'warn',
        // suppress error on redundant type hints
        '@typescript-eslint/no-inferrable-types': 'off',
        // allow ts ignore comment
        '@typescript-eslint/ban-ts-comment': 'off'
    }
}
