// ==========================================
// VELLOX - STATIC REACT APPLICATION
// ==========================================
// This file contains all React components combined into one.
// It is compiled in the browser by Babel via CDN.

const { useState, useRef, useEffect } = React;

// --- VelloxLogo Component ---
function VelloxLogo({ size = 36 }) {
    return (
        <div className="vellox-logo" style={{ width: size, height: size }}>
            <svg
                viewBox="0 0 120 120"
                xmlns="http://www.w3.org/2000/svg"
                className="vellox-logo-svg"
            >
                <defs>
                    <linearGradient id="logoGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#00d4ff" />
                        <stop offset="50%" stopColor="#a855f7" />
                        <stop offset="100%" stopColor="#e74c8a" />
                    </linearGradient>
                    <linearGradient id="logoGradReverse" x1="100%" y1="0%" x2="0%" y2="100%">
                        <stop offset="0%" stopColor="#00d4ff" />
                        <stop offset="100%" stopColor="#a855f7" />
                    </linearGradient>
                    <filter id="logoGlow">
                        <feGaussianBlur stdDeviation="3" result="blur" />
                        <feMerge>
                            <feMergeNode in="blur" />
                            <feMergeNode in="SourceGraphic" />
                        </feMerge>
                    </filter>
                </defs>

                <polygon
                    points="60,5 110,30 110,90 60,115 10,90 10,30"
                    fill="none"
                    stroke="url(#logoGrad)"
                    strokeWidth="2.5"
                    opacity="0.8"
                />
                <polygon
                    points="60,12 104,34 104,86 60,108 16,86 16,34"
                    fill="rgba(168, 85, 247, 0.08)"
                    stroke="none"
                />

                <g filter="url(#logoGlow)">
                    <path
                        d="M 35,32 L 60,88 L 85,32"
                        fill="none"
                        stroke="url(#logoGrad)"
                        strokeWidth="7"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                    />
                    <path
                        d="M 44,42 L 60,76 L 76,42"
                        fill="none"
                        stroke="url(#logoGradReverse)"
                        strokeWidth="2.5"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        opacity="0.6"
                    />
                </g>

                <circle cx="60" cy="5" r="2.5" fill="#00d4ff" opacity="0.9" />
                <circle cx="110" cy="30" r="2" fill="#a855f7" opacity="0.7" />
                <circle cx="110" cy="90" r="2" fill="#e74c8a" opacity="0.7" />
                <circle cx="60" cy="115" r="2.5" fill="#e74c8a" opacity="0.9" />
                <circle cx="10" cy="90" r="2" fill="#a855f7" opacity="0.7" />
                <circle cx="10" cy="30" r="2" fill="#00d4ff" opacity="0.7" />
            </svg>
        </div>
    );
}

// --- Navbar Component ---
function Navbar() {
    return (
        <nav className="navbar" id="top">
            <div className="navbar-brand">
                <VelloxLogo size={38} />
                <div className="navbar-text">
                    <span className="navbar-title">Vellox</span>
                    <span className="navbar-subtitle">Transform Data into Insight</span>
                </div>
            </div>
            <div className="navbar-links">
                <a href="#upload" className="nav-link nav-link-cta">Upload CSV</a>
            </div>
        </nav>
    );
}

// --- Hero Component ---
function Hero() {
    return (
        <section className="hero">
            <p className="hero-tagline">
                <span className="hero-sparkle">✦</span>
                Powered by Simplicity
                <span className="hero-sparkle">✦</span>
            </p>

            <h1 className="hero-heading">
                <span className="word-gradient">See</span> what your data
                <br />
                <span className="word-accent">really</span> means
            </h1>

            <p className="hero-subtitle">
                Drop a CSV and watch it transform into a living, breathing visual story.
                No setup. No complexity. Just clarity.
            </p>

            <div className="hero-actions">
                <a href="#upload" className="hero-cta">
                    <span className="cta-icon">⬆</span>
                    Get Started
                </a>
            </div>

            <div className="hero-stats">
                <div className="stat">
                    <span className="stat-value">CSV</span>
                    <span className="stat-label">File Support</span>
                </div>
                <div className="stat-divider"></div>
                <div className="stat">
                    <span className="stat-value">Instant</span>
                    <span className="stat-label">Processing</span>
                </div>
                <div className="stat-divider"></div>
                <div className="stat">
                    <span className="stat-value">Free</span>
                    <span className="stat-label">Always</span>
                </div>
            </div>
        </section>
    );
}

// --- CsvUpload Component ---
function CsvUpload() {
    const [dragging, setDragging] = useState(false);
    const [fileName, setFileName] = useState('');
    const fileInputRef = useRef(null);

    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragging(false);
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            setFileName(files[0].name);
        }
    };

    const handleFileChange = (e) => {
        if (e.target.files.length > 0) {
            setFileName(e.target.files[0].name);
        }
    };

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    return (
        <section className="csv-upload-section" id="upload">
            <h2 className="section-heading">
                <span className="section-icon">📊</span>
                Upload Your Data
            </h2>
            <p className="section-desc">
                Drag and drop your CSV file below, or click to browse
            </p>

            <div className="csv-upload">
                <div
                    className={`csv-upload-zone ${dragging ? 'dragging' : ''} ${fileName ? 'has-file' : ''}`}
                    onDragEnter={handleDragEnter}
                    onDragLeave={handleDragLeave}
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    onClick={handleClick}
                >
                    <div className="corner-accent top-left"></div>
                    <div className="corner-accent top-right"></div>
                    <div className="corner-accent bottom-left"></div>
                    <div className="corner-accent bottom-right"></div>

                    <div className="upload-icon-wrapper">
                        <svg
                            className="csv-upload-icon"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.5"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                            <polyline points="17 8 12 3 7 8" />
                            <line x1="12" y1="3" x2="12" y2="15" />
                        </svg>
                        <div className="upload-ring"></div>
                    </div>

                    {fileName ? (
                        <div className="file-info">
                            <p className="file-name">📄 {fileName}</p>
                            <p className="file-hint">Click to change file</p>
                        </div>
                    ) : (
                        <React.Fragment>
                            <p className="csv-upload-title">Drop your CSV into the void</p>
                            <p className="csv-upload-hint">
                                or click to browse <span>• CSV files only</span>
                            </p>
                        </React.Fragment>
                    )}

                    <input
                        ref={fileInputRef}
                        type="file"
                        accept=".csv"
                        className="csv-upload-input"
                        onChange={handleFileChange}
                    />
                </div>
            </div>
        </section>
    );
}

// --- Footer Component ---
function Footer() {
    const year = new Date().getFullYear();

    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-brand">
                    <span className="footer-logo">Vellox</span>
                    <span className="footer-dot">•</span>
                    <span className="footer-tagline">Transform Data into Insight</span>
                </div>
                <p className="footer-copy">
                    © {year} Vellox. Built with React.
                </p>
            </div>
        </footer>
    );
}

// --- AnimatedBackground Component ---
function AnimatedBackground() {
    return (
        <div className="animated-bg">
            <div className="stars-layer-1"></div>
            <div className="stars-layer-2"></div>
            <div className="stars-layer-3"></div>
            <div className="cyber-grid"></div>
            <div className="cyber-horizon"></div>
            <div className="orb orb-1"></div>
            <div className="orb orb-2"></div>
        </div>
    );
}

// --- Main App Component ---
function App() {
    return (
        <div className="app">
            <AnimatedBackground />
            <Navbar />
            <main className="app-content">
                <Hero />
                <CsvUpload />
            </main>
            <Footer />
        </div>
    );
}

// Render the application
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
