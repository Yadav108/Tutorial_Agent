from content.models import Topic, Example, Exercise

def create_modern_development_content() -> Topic:
    """Create and return tutorial content on Modern JavaScript Development."""
    return Topic(
        title="Modern JavaScript Development",
        description="Explore tools and practices used in modern JavaScript development.",
        content="""
        <h1>Modern JavaScript Development</h1>
        <p>JavaScript has evolved significantly, with new tools, libraries, and frameworks that make development faster, more efficient, and more powerful. Key aspects include module bundling, transpiling, package management, and working with modern frameworks and libraries.</p>

        <h2>Module Bundlers</h2>
        <p>Tools like Webpack, Parcel, and Vite bundle JavaScript modules into a single file, improving efficiency by combining code dependencies and enabling optimizations for faster loading times.</p>

        <h2>Transpiling with Babel</h2>
        <p>Babel allows developers to use the latest JavaScript features by converting (or "transpiling") them into code compatible with older browsers. Babel is essential for modern development as it enables backward compatibility.</p>

        <h2>Package Management with npm and Yarn</h2>
        <p>npm (Node Package Manager) and Yarn are tools for managing dependencies in JavaScript projects, making it easier to install, update, and configure packages for development.</p>

        <h2>Frameworks and Libraries</h2>
        <p>Popular libraries and frameworks such as React, Vue, and Angular provide structures and features that simplify building complex applications.</p>

        <h2>Automated Testing</h2>
        <p>Testing frameworks like Jest, Mocha, and Cypress enable automated testing, making it easier to ensure code reliability and maintainability.</p>

        <h2>Version Control with Git</h2>
        <p>Git is a version control system that helps track changes and collaborate with others on code, and GitHub, GitLab, and Bitbucket provide hosting for Git repositories.</p>
        """,
        examples=[
            Example(
                title="Basic Webpack Configuration",
                code="""
// webpack.config.js
const path = require('path');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist')
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader'
                }
            }
        ]
    }
};
""",
                explanation="This Webpack configuration specifies the entry and output files, and includes a rule to use Babel for transpiling modern JavaScript syntax."
            ),
            Example(
                title="Using Babel to Transpile Code",
                code="""
// .babelrc
{
    "presets": ["@babel/preset-env"]
}

// Command to install Babel
// npm install --save-dev @babel/core @babel/preset-env babel-loader
""",
                explanation="The .babelrc file contains Babel presets, which specify the features to transpile. Here, @babel/preset-env includes syntax compatible with most browsers."
            ),
            Example(
                title="Installing Packages with npm",
                code="""
// Initialize npm in the project
// npm init -y

// Install React
// npm install react react-dom
""",
                explanation="npm init initializes the package.json file to manage dependencies, while `npm install` adds specified packages to the project."
            )
        ],
        exercises=[
            Exercise(
                title="Set Up Webpack and Babel",
                description="Create a basic JavaScript project setup using Webpack and Babel.",
                starter_code="""// Steps:
// 1. Initialize npm in the project.
// 2. Install Webpack, Babel, and their respective loaders and presets.
// 3. Configure Webpack and Babel to transpile ES6+ code to ES5 compatible code.
""",
                solution="""// Solution setup instructions:
// 1. Run: npm init -y
// 2. Install dependencies: npm install webpack webpack-cli @babel/core babel-loader @babel/preset-env --save-dev
// 3. Create a basic Webpack config file with entry, output, and module rules.
// 4. Set up a .babelrc file with @babel/preset-env.
""",
                difficulty="Intermediate",
                hints=[
                    "Use npm init to start a new project.",
                    "Set entry and output paths in Webpack config.",
                    "Configure Babel with @babel/preset-env to support ES6+ syntax."
                ]
            ),
            Exercise(
                title="Create a Basic React App",
                description="Set up a basic React app with JSX support using Babel and Webpack.",
                starter_code="""// Steps:
// 1. Initialize npm and install React, ReactDOM, Webpack, and Babel.
// 2. Configure Webpack to transpile JSX using Babel.
// 3. Create a simple React component and render it to the DOM.
""",
                solution="""// Solution setup instructions:
// 1. Run: npm init -y
// 2. Install dependencies: npm install react react-dom webpack webpack-cli @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev
// 3. Configure Webpack with entry, output, and module rules for JSX.
// 4. Create an App component and render it in an HTML file.
""",
                difficulty="Advanced",
                hints=[
                    "Use `@babel/preset-react` for JSX syntax.",
                    "Set up Webpack entry and output paths.",
                    "Create an HTML file to render the React component."
                ]
            )
        ],
        best_practices=[
            "Use Webpack to bundle and optimize JavaScript files.",
            "Use Babel to ensure code compatibility across browsers.",
            "Manage dependencies carefully with npm or Yarn.",
            "Write tests for critical functions and components.",
            "Utilize version control (e.g., Git) for better code management.",
            "Organize code in modules for maintainability and reusability."
        ]
    )
