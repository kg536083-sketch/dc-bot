<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>Prisma X Content Maker by Ayush</title>

    <!-- Google Fonts for UI and Canvas -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link
        href="https://fonts.googleapis.com/css2?family=Amatic+SC&family=Anton&family=Architects+Daughter&family=Audiowide&family=Bebas+Neue&family=Caveat&family=Caveat+Brush&family=Cinzel:wght@400;600;700;900&family=Cinzel+Decorative&family=Coming+Soon&family=Cormorant+Garamond&family=Covered+By+Your+Grace&family=Dancing+Script&family=Fredoka+One&family=Gloria+Hallelujah&family=Gochi+Hand&family=Handlee&family=IM+Fell+English&family=Indie+Flower&family=Just+Another+Hand&family=Kalam&family=Libre+Baskerville&family=Lilita+One&family=Montserrat:wght@400;600;700&family=Nunito:wght@400;600;700&family=Orbitron&family=Oswald&family=Pacifico&family=Patrick+Hand&family=Playfair+Display&family=Poppins:wght@400;600;700&family=Quicksand:wght@400;600;700&family=Raleway:wght@400;600;700&family=Reenie+Beanie&family=Righteous&family=Rock+Salt&family=Satisfy&family=Shadows+Into+Light&display=swap"
        rel="stylesheet">

    <!-- FontAwesome for Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <!-- Fabric.js 5.3 -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"></script>

    <!-- Pickr Color Picker -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@simonwep/pickr/dist/themes/nano.min.css"/>
    <script src="https://cdn.jsdelivr.net/npm/@simonwep/pickr/dist/pickr.min.js"></script>

    <link rel="stylesheet" href="style.css">
</head>

<body>
    <!-- Background Particles -->
    <div id="particles"></div>

    <!-- Startup Ratio Modal -->
    <div id="startup_modal" class="modal-overlay">
        <div class="modal-content gold-theme">
            <h1>PrismaX Content Maker by Ayush</h1>
            <p>Select your canvas ratio to begin</p>
            <div class="ratio-grid">
                <button class="ratio-btn" data-width="1080" data-height="1080">
                    <div class="shape square"></div>1:1 (Square)
                </button>
                <button class="ratio-btn" data-width="1920" data-height="1080">
                    <div class="shape landscape"></div>16:9 (Video)
                </button>
                <button class="ratio-btn" data-width="1080" data-height="1920">
                    <div class="shape portrait"></div>9:16 (Story)
                </button>
                <button class="ratio-btn" data-width="1080" data-height="1440">
                    <div class="shape threefour"></div>3:4 (Portrait)
                </button>
            </div>
            <div class="custom-ratio">
                <input type="number" id="custom_w" placeholder="W" value="800">
                <span style="color:var(--primary-gold)">x</span>
                <input type="number" id="custom_h" placeholder="H" value="600">
                <button id="btn_custom_ratio" class="gold-btn">Set Custom</button>
            </div>
        </div>
    </div>

    <!-- Main App Wrapper -->
    <div id="app" class="hidden">

        <!-- Left Sidebar / Bottom Sheet Mobile -->
        <aside id="left_sidebar" class="sidebar tools-sidebar">
            <div class="panel-header mobile-only">
                <div style="display:flex; gap: 15px; align-items:center;">
                    <button class="close-sheet back-btn" style="font-size:1.2rem; padding:5px;"><i
                            class="fa-solid fa-arrow-left"></i></button>
                    <h3 id="mobile_tools_title" style="margin:0; font-size:1.2rem;">TOOLS</h3>
                </div>
                <button class="close-sheet" style="font-size:1.5rem; padding:5px;"><i
                        class="fa-solid fa-times"></i></button>
            </div>
            <div class="brand-title-img desktop-only"
                style="text-align: center; padding: 20px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
                <img src="assets/logos/logo-prismax-02.png" alt="PRISMA X"
                    style="max-width: 80%; height: auto; max-height: 60px;">
            </div>
            <nav class="tool-nav desktop-only">
                <button id="btn_theme_toggle_desk" class="nav-tab"><i class="fa-solid fa-circle-half-stroke"></i>
                    Theme</button>
                <button class="nav-tab" data-target="panel_assets"><i class="fa-solid fa-gem"></i> Assets</button>
                <button class="nav-tab active" data-target="panel_text"><i class="fa-solid fa-font"></i> Text</button>
                <button class="nav-tab" data-target="panel_bg"><i class="fa-solid fa-fill-drip"></i> Background</button>
                <button class="nav-tab" data-target="panel_shapes"><i class="fa-solid fa-shapes"></i> Shapes</button>
                <button class="nav-tab" data-target="panel_arrows"><i class="fa-solid fa-arrow-right-long"></i>
                    Arrow</button>
                <button class="nav-tab" data-target="panel_layers"><i class="fa-solid fa-layer-group"></i>
                    Layers</button>
            </nav>
            <div class="panel-container">
                <!-- Assets Panel -->
                <div id="panel_assets" class="panel">
                    <div
                        style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; border-bottom: 1px solid var(--border-gold); padding-bottom: 5px;">
                        <h3 style="margin:0; border:none;">Library</h3>
                        <div style="display:flex; gap: 5px;">
                            <label class="gold-btn outline" style="margin:0; width:auto; height:auto; padding:5px 10px; font-size:0.7rem; cursor:pointer;">
                                <i class="fa-solid fa-upload"></i> Upload
                                <input type="file" id="upload_my_asset" accept="image/png, image/jpeg, image/svg+xml" hidden>
                            </label>
                            <button onclick="loadAssets()" class="gold-btn outline"
                                style="width:auto; height:auto; padding:5px 10px; font-size:0.7rem;"><i
                                    class="fa-solid fa-arrows-rotate"></i> Sync</button>
                        </div>
                    </div>

                    <div class="tab-subnav">
                        <button class="sub-tab active" data-sub="assets_off">Official</button>
                        <button class="sub-tab" data-sub="assets_my">Uploads</button>
                        <button class="sub-tab" data-sub="assets_web">Search</button>
                    </div>

                    <!-- Official Assets -->
                    <div id="assets_off" class="sub-panel active custom-scrollbar"
                        style="max-height: calc(100vh - 350px); overflow-y: auto;">
                        <h4 class="asset-cat-title">Logos</h4>
                        <div id="grid_logos" class="asset-grid"></div>
                        <h4 class="asset-cat-title mt-20">Stickers</h4>
                        <div id="grid_stickers" class="asset-grid"></div>
                        <h4 class="asset-cat-title mt-20">Backgrounds</h4>
                        <div id="grid_backgrounds_gallery" class="asset-grid"></div>
                        <h4 class="asset-cat-title mt-20">Blocks</h4>
                        <div id="grid_blocks" class="asset-grid">
                            <div class="asset-item" onclick="addBlock('rect')"
                                style="background:var(--primary-gold); border-radius:4px; border:2px solid #000;"><span
                                    style="background:rgba(0,0,0,0.5)">Rect</span></div>
                            <div class="asset-item" onclick="addBlock('square')"
                                style="background:var(--primary-gold); border-radius:2px; width:40px; height:40px; margin:auto; border:2px solid #000;">
                                <span style="background:rgba(0,0,0,0.5)">Square</span>
                            </div>
                            <div class="asset-item" onclick="addBlock('circle')"
                                style="background:var(--primary-gold); border-radius:50%; border:2px solid #000;"><span
                                    style="background:rgba(0,0,0,0.5)">Circle</span></div>
                            <div class="asset-item" onclick="addBlock('diamond')"
                                style="background:var(--primary-gold); clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%); border:2px solid #000;">
                                <span style="background:rgba(0,0,0,0.5)">Diamond</span>
                            </div>
                            <div class="asset-item" onclick="addBlock('rhomboid')"
                                style="background:var(--primary-gold); clip-path: polygon(25% 0%, 100% 0%, 75% 100%, 0% 100%); border:2px solid #000;">
                                <span style="background:rgba(0,0,0,0.5)">Rhombus</span>
                            </div>
                            <div class="asset-item" onclick="addBlock('clipped')"
                                style="background:var(--primary-gold); clip-path: polygon(25% 0%, 75% 0%, 100% 25%, 100% 75%, 75% 100%, 25% 100%, 0% 75%, 0% 25%); border:2px solid #000;">
                                <span style="background:rgba(0,0,0,0.5)">Clipped</span>
                            </div>
                        </div>
                        <h4 class="asset-cat-title mt-20">Elements</h4>
                        <div id="grid_elements" class="asset-grid"></div>
                    </div>

                    <!-- My Uploads -->
                    <div id="assets_my" class="sub-panel custom-scrollbar" style="max-height: calc(100vh - 350px); overflow-y: auto;">
                        <p class="helper-text" style="font-size:0.8rem; opacity:0.7; text-align:center;">Your custom uploaded images will automatically appear here!</p>
                        <div id="my_assets_grid" class="asset-grid mt-10"></div>
                    </div>

                    <!-- Web Search -->
                    <div id="assets_web" class="sub-panel">
                        <div class="search-container mb-15">
                            <div style="display:flex; gap:10px; margin-bottom:8px;">
                                <select id="asset_search_source"
                                    style="background:var(--bg-dark); color:var(--primary-gold); border:1px solid var(--border-gold); border-radius:8px; padding:5px 10px; font-size:0.75rem; width: 100%;">
                                    <option value="pixabay">Pixabay (Photos)</option>
                                    <option value="openverse">Openverse (Free CC)</option>
                                    <option value="icons">Iconify (SVG Icons)</option>
                                </select>
                            </div>
                            <div style="position:relative;">
                                <input type="text" id="asset_search_input" placeholder="Search the web..."
                                    style="width:100%; padding:12px 40px 12px 15px; background:rgba(255,255,255,0.05); border:1px solid var(--border-gold); border-radius:8px; color:#fff; font-size:0.9rem;">
                                <i class="fa-solid fa-magnifying-glass"
                                    style="position:absolute; right:15px; top:50%; transform:translateY(-50%); color:var(--primary-gold); cursor:pointer;"
                                    id="btn_do_search"></i>
                            </div>
                        </div>
                        <div id="grid_search_results" class="asset-grid custom-scrollbar"
                            style="max-height: calc(100vh - 450px); overflow-y: auto;">
                            <div style="text-align:center; padding:40px; opacity:0.3; font-size:0.8rem;">Enter keywords
                                to find thousands of assets</div>
                        </div>
                    </div>
                </div>
                <!-- Text Panel -->
                <div id="panel_text" class="panel">
                    <h3>Text Tool</h3>
                    <div class="grid-3 mb-15">
                        <button id="btn_add_heading" class="gold-btn" style="font-size:0.9rem; padding:10px 5px"
                            title="Heading">H1</button>
                        <button id="btn_add_subheading" class="gold-btn outline"
                            style="font-size:0.8rem; padding:10px 5px" title="Subheading">H2</button>
                        <button id="btn_add_body" class="gold-btn outline" style="font-size:0.8rem; padding:10px 5px"
                            title="Body Text">Body</button>
                    </div>
                    <div class="font-search">
                        <input type="text" id="font_search_input" placeholder="Search fonts...">
                    </div>
                    <label class="gold-btn block-btn mb-15 outline">
                        <i class="fa-solid fa-upload"></i> Upload Extra Font
                        <input type="file" id="upload_own_font" accept=".ttf,.otf" hidden>
                    </label>
                    <div id="font_list" class="font-list custom-scrollbar"></div>
                </div>

                <!-- Background Panel -->
                <div id="panel_bg" class="panel">
                    <h3>Canvas Background</h3>
                    <div class="bg-section">
                        <h4>Solid Colors</h4>
                        <div class="color-grid" id="bg_solid_grid"></div>
                        <div class="input-group mt-10">
                            <label>Pick Custom Color</label>
                            <input type="color" id="bg_solid_picker" value="#ffffff"
                                style="height:38px; min-height:auto;">
                        </div>
                    </div>
                    <div class="bg-section">
                        <h4>Gradients</h4>
                        <div class="gradient-grid" id="bg_grad_grid"></div>
                        <div class="mt-10"
                            style="background:rgba(212,175,55,0.05); padding:10px; border-radius:8px; border:1px solid var(--border-gold);">
                            <label
                                style="font-size:0.8rem; color:var(--primary-gold); font-weight:bold; display:block; margin-bottom:8px;">Custom
                                Gradient Designer</label>
                            <div class="grid-2">
                                <div class="input-group">
                                    <label style="font-size:0.7rem;">Start</label>
                                    <input type="color" id="bg_grad_start" value="#D4AF37"
                                        style="height:32px; min-height:auto;">
                                </div>
                                <div class="input-group">
                                    <label style="font-size:0.7rem;">End</label>
                                    <input type="color" id="bg_grad_end" value="#000000"
                                        style="height:32px; min-height:auto;">
                                </div>
                            </div>
                            <button id="btn_apply_custom_grad" class="gold-btn block-btn mt-5 small"
                                style="min-height:32px; font-size:0.8rem;">Apply Custom</button>
                        </div>
                    </div>
                    <div class="bg-section">
                        <h4>Official Backgrounds</h4>
                        <div id="grid_backgrounds" class="asset-grid"></div>
                    </div>
                    <div class="bg-section">
                        <label class="gold-btn block-btn mb-10"><i class="fa-solid fa-images"></i> Upload Image
                            <input type="file" id="bg_image_upload" accept="image/*" hidden>
                        </label>
                        <button id="btn_remove_bg" class="gold-btn block-btn danger-outline"><i
                                class="fa-solid fa-eraser"></i> Clear Background</button>
                    </div>
                </div>

                <!-- Shapes Panel -->
                <div id="panel_shapes" class="panel">
                    <h3>Shapes</h3>
                    <div class="bg-section mt-10 custom-scrollbar"
                        style="max-height: calc(100vh - 250px); overflow-y: auto;">
                        <h4 style="font-size:0.75rem; opacity:0.6; margin-bottom:8px;">Basic Shapes</h4>
                        <div class="grid-4 mb-10">
                            <button id="btn_add_rect" class="shape-btn" title="Rectangle"><i
                                    class="fa-solid fa-square"></i></button>
                            <button id="btn_add_rounded_rect" class="shape-btn" title="Rounded Rectangle"><i
                                    class="fa-solid fa-square" style="border-radius:4px;"></i></button>
                            <button id="btn_add_circle" class="shape-btn" title="Circle"><i
                                    class="fa-solid fa-circle"></i></button>
                            <button id="btn_add_ring" class="shape-btn" title="Ring"><i
                                    class="fa-regular fa-circle"></i></button>
                            <button id="btn_add_diamond" class="shape-btn" title="Diamond"><i class="fa-solid fa-square"
                                    style="transform: rotate(45deg); font-size:0.8em;"></i></button>
                            <button id="btn_add_triangle" class="shape-btn" title="Triangle"><i
                                    class="fa-solid fa-caret-up"></i></button>
                            <button id="btn_add_triangle_down" class="shape-btn" title="Triangle Down"><i
                                    class="fa-solid fa-caret-down"></i></button>
                            <button id="btn_add_triangle_right" class="shape-btn" title="Right Triangle"><i
                                    class="fa-solid fa-caret-right"></i></button>
                        </div>

                        <h4 style="font-size:0.75rem; opacity:0.6; margin-bottom:8px;">Polygons</h4>
                        <div class="grid-4 mb-10">
                            <button id="btn_add_pentagon" class="shape-btn" title="Pentagon"><i class="fa-solid fa-play"
                                    style="transform: rotate(-90deg);"></i></button>
                            <button id="btn_add_hexagon" class="shape-btn" title="Hexagon"><i
                                    class="fa-solid fa-cube"></i></button>
                            <button id="btn_add_octagon" class="shape-btn" title="Octagon"><i
                                    class="fa-solid fa-stop"></i></button>
                            <button id="btn_add_star" class="shape-btn" title="Star"><i
                                    class="fa-solid fa-star"></i></button>
                            <button id="btn_add_star4" class="shape-btn" title="4-Point Star"><i
                                    class="fa-solid fa-diamond"></i></button>
                            <button id="btn_add_star6" class="shape-btn" title="6-Point Star"><i
                                    class="fa-solid fa-asterisk"></i></button>
                            <button id="btn_add_cross" class="shape-btn" title="Cross / Plus"><i
                                    class="fa-solid fa-plus"></i></button>
                            <button id="btn_add_parallelogram" class="shape-btn" title="Parallelogram"><i
                                    class="fa-solid fa-bars" style="transform: skewX(-15deg);"></i></button>
                        </div>

                        <h4 style="font-size:0.75rem; opacity:0.6; margin-bottom:8px;">Special Shapes</h4>
                        <div class="grid-4 mb-10">
                            <button id="btn_add_heart" class="shape-btn" title="Heart"><i
                                    class="fa-solid fa-heart"></i></button>
                            <button id="btn_add_cloud" class="shape-btn" title="Cloud"><i
                                    class="fa-solid fa-cloud"></i></button>
                            <button id="btn_add_lightning" class="shape-btn" title="Lightning Bolt"><i
                                    class="fa-solid fa-bolt"></i></button>
                            <button id="btn_add_moon" class="shape-btn" title="Crescent Moon"><i
                                    class="fa-solid fa-moon"></i></button>
                            <button id="btn_add_speech" class="shape-btn" title="Speech Bubble"><i
                                    class="fa-solid fa-comment"></i></button>
                            <button id="btn_add_badge" class="shape-btn" title="Badge"><i
                                    class="fa-solid fa-certificate"></i></button>
                            <button id="btn_add_shield" class="shape-btn" title="Shield"><i
                                    class="fa-solid fa-shield"></i></button>
                            <button id="btn_add_explosion" class="shape-btn" title="Explosion"><i
                                    class="fa-solid fa-burst"></i></button>
                        </div>

                        <h4 style="font-size:0.75rem; opacity:0.6; margin-bottom:8px;">Arrow Shapes</h4>
                        <div class="grid-4 mb-10">
                            <button id="btn_add_arrow_right" class="shape-btn" title="Arrow Right"><i
                                    class="fa-solid fa-arrow-right"></i></button>
                            <button id="btn_add_arrow_left" class="shape-btn" title="Arrow Left"><i
                                    class="fa-solid fa-arrow-left"></i></button>
                            <button id="btn_add_arrow_up" class="shape-btn" title="Arrow Up"><i
                                    class="fa-solid fa-arrow-up"></i></button>
                            <button id="btn_add_arrow_down" class="shape-btn" title="Arrow Down"><i
                                    class="fa-solid fa-arrow-down"></i></button>
                            <button id="btn_add_chevron_right" class="shape-btn" title="Chevron Right"><i
                                    class="fa-solid fa-chevron-right"></i></button>
                            <button id="btn_add_double_arrow" class="shape-btn" title="Double Arrow"><i
                                    class="fa-solid fa-arrows-left-right"></i></button>
                            <button id="btn_add_curved_arrow" class="shape-btn" title="Curved Arrow"><i
                                    class="fa-solid fa-rotate-right"></i></button>
                            <button id="btn_add_bend_arrow" class="shape-btn" title="Bend Arrow"><i
                                    class="fa-solid fa-share"></i></button>
                        </div>

                        <h4 style="font-size:0.75rem; opacity:0.6; margin-bottom:8px;">Lines & Dividers</h4>
                        <div class="grid-4 mb-10">
                            <button id="btn_add_line" class="shape-btn" title="Straight Line"><i
                                    class="fa-solid fa-minus"></i></button>
                            <button id="btn_add_dashed_line" class="shape-btn" title="Dashed Line"><i
                                    class="fa-solid fa-ellipsis"></i></button>
                            <button id="btn_add_dotted_line" class="shape-btn" title="Dotted Line"><i
                                    class="fa-solid fa-grip-lines"></i></button>
                            <button id="btn_add_thick_line" class="shape-btn" title="Thick Line"><i
                                    class="fa-solid fa-ruler-horizontal"></i></button>
                            <button id="btn_add_bracket_left" class="shape-btn" title="Left Bracket"><span
                                    style="font-size:1.4rem; font-weight:200;">{</span></button>
                            <button id="btn_add_bracket_right" class="shape-btn" title="Right Bracket"><span
                                    style="font-size:1.4rem; font-weight:200;">}</span></button>
                            <button id="btn_add_divider_ornate" class="shape-btn" title="Ornate Divider"><i
                                    class="fa-solid fa-grip-lines-vertical"></i></button>
                            <button id="btn_add_wave_line" class="shape-btn" title="Wave Line"><i
                                    class="fa-solid fa-water"></i></button>
                        </div>

                        <h4 style="font-size:0.75rem; opacity:0.6; margin-bottom:8px;">Design Icons</h4>
                        <div class="grid-4 mb-10">
                            <button id="btn_add_checkmark" class="shape-btn" title="Checkmark"><i
                                    class="fa-solid fa-check"></i></button>
                            <button id="btn_add_xmark" class="shape-btn" title="X Mark"><i
                                    class="fa-solid fa-xmark"></i></button>
                            <button id="btn_add_location" class="shape-btn" title="Location Pin"><i
                                    class="fa-solid fa-location-dot"></i></button>
                            <button id="btn_add_bookmark" class="shape-btn" title="Bookmark"><i
                                    class="fa-solid fa-bookmark"></i></button>
                            <button id="btn_add_ribbon" class="shape-btn" title="Ribbon Banner"><i
                                    class="fa-solid fa-ribbon"></i></button>
                            <button id="btn_add_trophy" class="shape-btn" title="Trophy"><i
                                    class="fa-solid fa-trophy"></i></button>
                            <button id="btn_add_crown" class="shape-btn" title="Crown"><i
                                    class="fa-solid fa-crown"></i></button>
                            <button id="btn_add_fire" class="shape-btn" title="Fire"><i
                                    class="fa-solid fa-fire"></i></button>
                        </div>
                    </div>
                </div>

                <!-- Arrow Panel -->
                <div id="panel_arrows" class="panel">
                    <h3>Lines & Arrows</h3>
                    <div class="bg-section mt-10">
                        <h4 style="font-size:0.75rem; opacity:0.6; margin-bottom:8px;">Connectors</h4>
                        <div class="grid-2 mt-10">
                            <button id="btn_add_free_arrow" class="gold-btn outline" style="font-size: 0.8rem;"><i
                                    class="fa-solid fa-arrow-right-long"></i> Free Arrow</button>
                            <button id="btn_add_arrow" class="gold-btn outline" style="font-size: 0.8rem;"><i
                                    class="fa-solid fa-link"></i> Smart Arrow</button>
                        </div>
                        <p class="helper-text mt-10" style="font-size: 0.8rem; opacity: 0.7;">Tap 'Smart Arrow' then tap
                            two
                            shapes to connect them.</p>
                    </div>
                </div>

                <!-- Layers Panel -->
                <div id="panel_layers" class="panel">
                    <h3>Layers</h3>
                    <div id="layers_list" class="layers-list custom-scrollbar"
                        style="max-height: calc(100vh - 250px); overflow-y: auto;">
                        <!-- Populated via JS -->
                    </div>
                </div>
            </div>

            <button class="nav-tab export-btn" id="btn_top_download"><i class="fa-solid fa-download"></i>
                Download</button>
        </aside>

        <!-- Canvas Area -->
        <main id="workspace">
            <!-- Top Horizontal Bar (Outside Canvas) -->
            <div class="top-row-controls">
                <div class="left-controls" style="display:flex; align-items:center; gap: 5px;">
                    <button id="btn_reset_studio" title="New Design (Clear All)"
                        style="color: #ff5555; font-family: 'Montserrat', sans-serif; font-weight: 800; font-size: 0.75rem; letter-spacing: 1px; width: auto; padding: 0 10px;">CLR</button>
                    <button id="btn_ratio_change" title="Change Canvas Ratio"><i
                            class="fa-solid fa-crop-simple"></i></button>
                    <button id="btn_undo" title="Undo (Ctrl+Z)"><i class="fa-solid fa-rotate-left"></i></button>
                    <button id="btn_redo" title="Redo (Ctrl+Y)"><i class="fa-solid fa-rotate-right"></i></button>

                    <button id="btn_save_progress" title="Save Progress (Merge All)"
                        style="color: var(--primary-gold); font-family: 'Montserrat', sans-serif; font-size: 0.75rem; width: auto; padding: 0 10px; margin-left: 5px; border: 1px solid var(--border-gold); background: var(--bg-dark); border-radius: 4px; border-width: 1px;">
                        <i class="fa-solid fa-layer-group" style="padding-right: 4px;"></i> Save Progress
                    </button>

                    <!-- Zoom Controls -->
                    <div
                        style="display:flex; align-items:center; background:var(--bg-dark); border-radius:15px; border:1px solid var(--border-gold); padding:0 5px; margin-left: 10px;">
                        <button id="btn_zoom_out" title="Zoom Out"
                            style="background:transparent; border:none; color:var(--primary-gold); font-size: 0.8rem; padding: 5px;"><i
                                class="fa-solid fa-magnifying-glass-minus"></i></button>
                        <span id="zoom_display"
                            style="color:var(--primary-gold); font-size:0.8rem; min-width: 45px; text-align:center; cursor:pointer;"
                            title="Click to Reset Zoom">100%</span>
                        <button id="btn_zoom_in" title="Zoom In"
                            style="background:transparent; border:none; color:var(--primary-gold); font-size: 0.8rem; padding: 5px;"><i
                                class="fa-solid fa-magnifying-glass-plus"></i></button>
                    </div>
                </div>
                <div class="right-controls" id="layer_controls">
                    <button id="btn_duplicate" title="Duplicate (Ctrl+D)"><i class="fa-regular fa-copy"></i></button>
                    <button id="btn_group" title="Group/Ungroup"><i class="fa-solid fa-object-group"></i></button>
                    <button id="btn_delete" class="danger-text" title="Delete"><i
                            class="fa-regular fa-trash-can"></i></button>
                </div>
            </div>

            <!-- Mobile Top Horizontal Tabs -->
            <nav id="mobile_tabs" class="mobile-tabs mobile-only">
                <button id="btn_theme_toggle_mob" class="nav-tab"><i class="fa-solid fa-circle-half-stroke"></i>
                    Theme</button>
                <button class="nav-tab" data-target="panel_assets"><i class="fa-solid fa-gem"></i> Assets</button>
                <button class="nav-tab active" data-target="panel_text"><i class="fa-solid fa-font"></i> Text</button>
                <button class="nav-tab" data-target="panel_shapes"><i class="fa-solid fa-shapes"></i> Shapes</button>
                <button class="nav-tab" data-target="panel_arrows"><i class="fa-solid fa-arrow-right-long"></i>
                    Arrow</button>
                <button class="nav-tab" data-target="panel_bg"><i class="fa-solid fa-fill-drip"></i> BG</button>
                <button class="nav-tab" data-target="panel_layers"><i class="fa-solid fa-layer-group"></i>
                    Layers</button>
                <button class="nav-tab" data-target="panel_props"><i class="fa-solid fa-sliders"></i> Edit</button>
                <button class="nav-tab" id="btn_mobile_download"><i class="fa-solid fa-download"></i> Download</button>
            </nav>

            <!-- Quick-Access Sub-Navigation (Mini Toolbar for all users) -->
            <div id="quick_access_toolbar" class="mobile-sub-tabs">
                <div class="sub-tabs-inner custom-scrollbar">
                    <!-- Populated dynamically via JS -->
                </div>
            </div>

            <div id="workspace_inner">
                <div id="canvas_container">
                    <canvas id="c"></canvas>
                </div>
            </div>
        </main>

        <!-- Right / Bottom Sheet Properties Panel -->
        <aside id="right_sidebar" class="sidebar props-sidebar">
            <div class="panel-header mobile-only">
                <div style="display:flex; gap: 15px; align-items:center;">
                    <button class="close-sheet back-btn" style="font-size:1.2rem; padding:5px;"><i
                            class="fa-solid fa-arrow-left"></i></button>
                    <h3 style="margin:0; font-size:1.2rem;">EDIT</h3>
                </div>
                <button class="close-sheet" style="font-size:1.5rem; padding:5px;"><i
                        class="fa-solid fa-times"></i></button>
            </div>
            <div id="properties_empty" class="empty-state">
                <p>Select an element to edit properties</p>
            </div>
            <div id="properties_editor" class="hidden custom-scrollbar">

                <!-- Layering Controls for Mobile -->
                <div class="prop-group mobile-only">
                    <h4>Arrangement</h4>
                    <div class="grid-2 mt-10">
                        <button id="btn_prop_bring_front" class="gold-btn outline small"><i
                                class="fa-solid fa-arrow-up-9-1"></i> Bring to Front</button>
                        <button id="btn_prop_send_back" class="gold-btn outline small"><i
                                class="fa-solid fa-arrow-down-9-1"></i> Send to Back</button>
                    </div>
                </div>

                <!-- Text Specific Properties (FIRST for text) -->
                <div id="text_properties" class="prop-group hidden">
                    <h4>Text Styles</h4>
                    <div class="grid-4 mb-10">
                        <button id="btn_text_bold" class="icon-toggle" title="Bold"><i
                                class="fa-solid fa-bold"></i></button>
                        <button id="btn_text_italic" class="icon-toggle" title="Italic"><i
                                class="fa-solid fa-italic"></i></button>
                        <button id="btn_text_underline" class="icon-toggle" title="Underline"><i
                                class="fa-solid fa-underline"></i></button>
                        <button id="btn_text_linethrough" class="icon-toggle" title="Strikethrough"><i
                                class="fa-solid fa-strikethrough"></i></button>

                        <button id="btn_align_left" class="icon-toggle align-btn" title="Align Left"><i
                                class="fa-solid fa-align-left"></i></button>
                        <button id="btn_align_center" class="icon-toggle align-btn" title="Align Center"><i
                                class="fa-solid fa-align-center"></i></button>
                        <button id="btn_align_right" class="icon-toggle align-btn" title="Align Right"><i
                                class="fa-solid fa-align-right"></i></button>
                        <button id="btn_align_justify" class="icon-toggle align-btn" title="Justify"><i
                                class="fa-solid fa-align-justify"></i></button>

                        <button id="btn_list_bullet" class="icon-toggle" title="Bullet List"
                            style="grid-column: span 2;"><i class="fa-solid fa-list-ul"></i> Bullet List</button>
                        <button id="btn_list_number" class="icon-toggle" title="Numbered List"
                            style="grid-column: span 2;"><i class="fa-solid fa-list-ol"></i> Number List</button>
                    </div>

                    <div class="input-group full-width">
                        <label>Font Size</label>
                        <input type="range" id="prop_fontsize_slider" min="10" max="300" value="40">
                        <input type="number" id="prop_fontsize_num" class="small-num" value="40">
                    </div>

                    <div class="input-group full-width">
                        <label>Font Color</label>
                        <input type="color" id="prop_textcolor" value="#D4AF37">
                    </div>

                    <div class="input-group full-width">
                        <label>Text Highlight</label>
                        <div style="display: flex; gap: 5px;">
                            <input type="color" id="prop_textbg" value="#000000" style="flex:1;">
                            <button id="btn_clear_textbg" class="gold-btn small" title="Make Transparent"><i
                                    class="fa-solid fa-times"></i></button>
                        </div>
                    </div>

                    <div class="input-group full-width">
                        <label>Letter Spacing</label>
                        <input type="range" id="prop_charspacing" min="-100" max="1000" value="0">
                    </div>

                    <div class="input-group full-width">
                        <label>Line Height</label>
                        <input type="range" id="prop_lineheight" min="0.5" max="3" step="0.1" value="1.16">
                    </div>

                    <div class="input-group full-width" style="display: none;">
                        <label><input type="checkbox" id="prop_textshadow"> Legacy Text Shadow</label>
                    </div>
                </div>

                <!-- Shape Specific Properties -->
                <div id="shape_properties" class="prop-group hidden">
                    <h4>Shape Styling</h4>
                    <div class="input-group full-width">
                        <label>Fill Color</label>
                        <div style="display: flex; gap: 5px;">
                            <input type="color" id="prop_shape_fill" value="#000000" style="flex:1;">
                            <button id="btn_clear_shape_fill" class="gold-btn small" title="Make Transparent"><i
                                    class="fa-solid fa-ban"></i></button>
                        </div>
                    </div>
                </div>

                <!-- Arrow / Line Properties -->
                <div id="arrow_properties" class="prop-group hidden">
                    <h4>Arrow Styles</h4>
                    <div class="input-group full-width">
                        <label>Color</label>
                        <input type="color" id="prop_arrow_color" value="#D4AF37">
                    </div>
                    <div class="input-group full-width">
                        <label>Thickness</label>
                        <input type="range" id="prop_arrow_width" min="1" max="50" value="4">
                    </div>
                    <div class="input-group full-width">
                        <label>Style</label>
                        <select id="prop_arrow_style">
                            <option value="straight">Straight</option>
                            <option value="curved">Curved</option>
                            <option value="elbow">Elbow (90°)</option>
                        </select>
                    </div>
                    <div class="input-group full-width">
                        <label>Start Head</label>
                        <select id="prop_arrow_head1">
                            <option value="none">None</option>
                            <option value="triangle">Triangle</option>
                            <option value="circle">Circle</option>
                            <option value="open">Open</option>
                        </select>
                    </div>
                    <div class="input-group full-width">
                        <label>End Head</label>
                        <select id="prop_arrow_head2">
                            <option value="triangle">Triangle</option>
                            <option value="circle">Circle</option>
                            <option value="open">Open</option>
                            <option value="none">None</option>
                        </select>
                    </div>
                </div>

                <!-- Gradient Fill (for shapes, text, elements) -->
                <div id="gradient_properties" class="prop-group hidden">
                    <h4><i class="fa-solid fa-paint-roller" style="margin-right:6px;"></i>Gradient Fill</h4>
                    <div class="input-group full-width">
                        <label>Start Color</label>
                        <input type="color" id="grad_color1" value="#D4AF37">
                    </div>
                    <div class="input-group full-width">
                        <label>End Color</label>
                        <input type="color" id="grad_color2" value="#ff4444">
                    </div>
                    <div class="input-group full-width">
                        <label>Direction</label>
                        <select id="grad_direction" style="width:100%;">
                            <option value="horizontal">↔ Horizontal</option>
                            <option value="vertical">↕ Vertical</option>
                            <option value="diagonal">↗ Diagonal</option>
                            <option value="radial">⊙ Radial</option>
                        </select>
                    </div>
                    <div style="display:flex; gap:8px; margin-top:8px;">
                        <button id="btn_apply_gradient" class="gold-btn" style="flex:1; padding:8px 0; font-size:0.8rem;"><i class="fa-solid fa-check"></i> Apply</button>
                        <button id="btn_clear_gradient" class="gold-btn outline" style="flex:1; padding:8px 0; font-size:0.8rem;"><i class="fa-solid fa-ban"></i> Clear</button>
                    </div>
                    <div id="gradient_preview" style="margin-top:10px; height:30px; border-radius:8px; border:1px solid var(--border-gold); background: linear-gradient(to right, #D4AF37, #ff4444);"></div>
                </div>

                <!-- Universal Border Properties -->
                <div class="prop-group" id="border_properties">
                    <h4>Border (Stroke)</h4>
                    <div class="input-group full-width">
                        <label>Border Color</label>
                        <div style="display: flex; gap: 5px;">
                            <input type="color" id="prop_border_color" value="#D4AF37" style="flex:1;">
                            <button id="btn_clear_border" class="gold-btn small" title="Remove Border"><i class="fa-solid fa-ban"></i></button>
                        </div>
                    </div>
                    <div class="input-group full-width mt-10">
                        <label>Border Thickness</label>
                        <input type="range" id="prop_border_width" min="0" max="50" value="0">
                        <div style="display:flex; justify-content:space-between; font-size:0.7rem; opacity:0.6;">
                            <span>None</span><span>Thick</span>
                        </div>
                    </div>
                </div>

                <!-- Corner Radius Properties -->
                <div id="corner_properties" class="prop-group hidden">
                    <h4>Corner Curving</h4>
                    <div class="input-group full-width" id="prop_corner_group">
                        <input type="range" id="prop_corner_radius" min="0" max="150" value="0">
                        <div style="display:flex; justify-content:space-between; font-size:0.7rem; opacity:0.6;">
                            <span>Sharp</span><span>Round</span>
                        </div>
                    </div>
                </div>

                <!-- Common Transform Properties (moved BELOW colors) -->
                <div class="prop-group">
                    <h4>Transform</h4>
                    <div class="grid-2">
                        <div class="input-group">
                            <label>X</label>
                            <input type="number" id="prop_x">
                        </div>
                        <div class="input-group">
                            <label>Y</label>
                            <input type="number" id="prop_y">
                        </div>
                        <div class="input-group">
                            <label>W</label>
                            <input type="number" id="prop_w">
                        </div>
                        <div class="input-group">
                            <label>H</label>
                            <input type="number" id="prop_h">
                        </div>
                        <div class="input-group full-width">
                            <label><input type="checkbox" id="prop_lock_ratio"> Lock Aspect Ratio</label>
                        </div>
                        <div class="input-group">
                            <label>Rotate &deg;</label>
                            <input type="number" id="prop_angle">
                        </div>
                        <div class="input-group full-width">
                            <label>Opacity %</label>
                            <input type="range" id="prop_opacity_slider" min="0" max="100" value="100">
                            <input type="number" id="prop_opacity_num" class="small-num" value="100" min="0" max="100">
                        </div>
                    </div>
                </div>

                <div class="prop-group">
                    <h4>Flip</h4>
                    <div class="grid-2">
                        <button id="btn_flip_x" class="gold-btn small"><i
                                class="fa-solid fa-arrows-left-right"></i></button>
                        <button id="btn_flip_y" class="gold-btn small"><i
                                class="fa-solid fa-arrows-up-down"></i></button>
                    </div>
                </div>

                <!-- Global Effects Properties -->
                <div class="prop-group">
                    <h4>Effects &amp; Shadows</h4>
                    <div class="input-group full-width">
                        <label>Shadow Color</label>
                        <div style="display: flex; gap: 5px;">
                            <input type="color" id="prop_shadow_color" value="#000000" style="flex:1;">
                            <button id="btn_clear_shadow" class="gold-btn small" title="Remove Shadow"><i
                                    class="fa-solid fa-ban"></i></button>
                        </div>
                    </div>
                    <div class="input-group full-width">
                        <label>Blur Intensity</label>
                        <input type="range" id="prop_shadow_blur" min="0" max="100" value="10">
                    </div>
                    <div class="grid-2">
                        <div class="input-group">
                            <label>Offset X</label>
                            <input type="number" id="prop_shadow_offset_x" value="5">
                        </div>
                        <div class="input-group">
                            <label>Offset Y</label>
                            <input type="number" id="prop_shadow_offset_y" value="5">
                        </div>
                    </div>

                    <!-- Quick 3D Shadow Presets -->
                    <h4 style="margin-top: 15px; font-size: 0.85rem;">Quick 3D Shadows</h4>
                    <div class="grid-3 mt-10" style="gap: 6px;">
                        <button id="btn_shadow_soft" class="shadow-preset-btn" title="Soft Shadow">
                            <div class="shadow-preview" style="box-shadow: 3px 4px 10px rgba(0,0,0,0.3);"></div>
                            <span>Soft</span>
                        </button>
                        <button id="btn_shadow_hard" class="shadow-preset-btn" title="Hard Shadow">
                            <div class="shadow-preview" style="box-shadow: 5px 5px 0px rgba(0,0,0,0.5);"></div>
                            <span>Hard</span>
                        </button>
                        <button id="btn_shadow_3d" class="shadow-preset-btn" title="3D Lift Effect">
                            <div class="shadow-preview" style="box-shadow: 0px 8px 20px rgba(0,0,0,0.35);"></div>
                            <span>3D Lift</span>
                        </button>
                        <button id="btn_shadow_long" class="shadow-preset-btn" title="Long Shadow">
                            <div class="shadow-preview" style="box-shadow: 8px 8px 2px rgba(0,0,0,0.25);"></div>
                            <span>Long</span>
                        </button>
                        <button id="btn_shadow_glow" class="shadow-preset-btn" title="Glow Effect">
                            <div class="shadow-preview" style="box-shadow: 0px 0px 15px rgba(212,175,55,0.6);"></div>
                            <span>Glow</span>
                        </button>
                        <button id="btn_shadow_neon" class="shadow-preset-btn" title="Neon Glow">
                            <div class="shadow-preview" style="box-shadow: 0px 0px 20px rgba(0,200,255,0.7);"></div>
                            <span>Neon</span>
                        </button>
                    </div>
                </div>

            </div>
        </aside>
    </div>

    <div id="toast" class="toast hidden"></div>

    <script src="app.js"></script>
</body>

</html>
