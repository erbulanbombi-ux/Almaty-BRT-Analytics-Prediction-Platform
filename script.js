```javascript
/* =====================================================
   ALMATY LRT — THREE.JS 3D VIEWER
===================================================== */

const container = document.getElementById("viewer");


// -----------------------------------------------------
// SCENE
// -----------------------------------------------------

const scene = new THREE.Scene();

scene.background = new THREE.Color(0x0f172a);


// -----------------------------------------------------
// CAMERA
// -----------------------------------------------------

const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
);

camera.position.set(7, 4, 9);


// -----------------------------------------------------
// RENDERER
// -----------------------------------------------------

const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true
});

renderer.setPixelRatio(
    Math.min(window.devicePixelRatio, 2)
);

renderer.setSize(
    container.clientWidth,
    container.clientHeight
);

renderer.shadowMap.enabled = true;

container.appendChild(renderer.domElement);


// -----------------------------------------------------
// LIGHTING
// -----------------------------------------------------

const ambientLight = new THREE.AmbientLight(
    0xffffff,
    1.5
);

scene.add(ambientLight);


const directionalLight = new THREE.DirectionalLight(
    0xffffff,
    3
);

directionalLight.position.set(
    5,
    10,
    7
);

directionalLight.castShadow = true;

scene.add(directionalLight);


const blueLight = new THREE.PointLight(
    0x38bdf8,
    5,
    20
);

blueLight.position.set(
    0,
    3,
    4
);

scene.add(blueLight);


// -----------------------------------------------------
// ORBIT CONTROLS
// -----------------------------------------------------

const controls = new THREE.OrbitControls(
    camera,
    renderer.domElement
);

controls.enableDamping = true;

controls.dampingFactor = 0.06;

controls.minDistance = 4;

controls.maxDistance = 16;

controls.target.set(
    0,
    1,
    0
);


// -----------------------------------------------------
// MATERIALS
// -----------------------------------------------------

const trainMaterial = new THREE.MeshStandardMaterial({
    color: 0x075985,

    metalness: 0.85,

    roughness: 0.2
});


const darkMaterial = new THREE.MeshStandardMaterial({
    color: 0x020617,

    metalness: 0.9,

    roughness: 0.15
});


const glassMaterial = new THREE.MeshPhysicalMaterial({
    color: 0x38bdf8,

    transparent: true,

    opacity: 0.35,

    metalness: 0.1,

    roughness: 0,

    transmission: 0.5
});


const neonMaterial = new THREE.MeshBasicMaterial({
    color: 0x38bdf8
});


// -----------------------------------------------------
// TRAIN
// -----------------------------------------------------

function createTrain() {

    const train = new THREE.Group();

    train.name = "train";


    // Main body

    const bodyGeometry =
        new THREE.BoxGeometry(
            7,
            1.8,
            2.2
        );

    const body = new THREE.Mesh(
        bodyGeometry,
        trainMaterial
    );

    body.position.y = 1.8;

    body.castShadow = true;

    train.add(body);


    // Roof

    const roofGeometry =
        new THREE.BoxGeometry(
            6.5,
            0.25,
            2
        );

    const roof = new THREE.Mesh(
        roofGeometry,
        darkMaterial
    );

    roof.position.y = 2.85;

    train.add(roof);


    // Front

    const frontGeometry =
        new THREE.BoxGeometry(
            0.3,
            1.5,
            2
        );

    const front = new THREE.Mesh(
        frontGeometry,
        glassMaterial
    );

    front.position.set(
        3.55,
        1.85,
        0
    );

    train.add(front);


    // Windows

    for (let i = -2.4; i <= 2.4; i += 1.2) {

        const windowGeometry =
            new THREE.BoxGeometry(
                0.85,
                0.75,
                0.04
            );

        const windowMaterial =
            new THREE.MeshStandardMaterial({
                color: 0x020617,

                metalness: 0.7,

                roughness: 0.1
            });


        const window1 = new THREE.Mesh(
            windowGeometry,
            windowMaterial
        );

        window1.position.set(
            i,
            2,
            1.12
        );

        train.add(window1);


        const window2 = window1.clone();

        window2.position.z = -1.12;

        train.add(window2);
    }


    // Wheels

    for (let x of [-2.3, 2.3]) {

        for (let z of [-0.9, 0.9]) {

            const wheelGeometry =
                new THREE.CylinderGeometry(
                    0.45,
                    0.45,
                    0.25,
                    32
                );

            const wheel =
                new THREE.Mesh(
                    wheelGeometry,
                    darkMaterial
                );

            wheel.rotation.x =
                Math.PI / 2;

            wheel.position.set(
                x,
                0.65,
                z
            );

            train.add(wheel);
        }
    }


    // Neon Apple symbol

    const apple = createApple();

    apple.position.set(
        0,
        1.8,
        1.16
    );

    train.add(apple);


    // Snow leopard symbol

    const leopard =
        createLeopard();

    leopard.position.set(
        -2,
        1.8,
        1.17
    );

    train.add(leopard);


    return train;
}


// -----------------------------------------------------
// APPLE SYMBOL
// -----------------------------------------------------

function createApple() {

    const group = new THREE.Group();

    const geometry =
        new THREE.SphereGeometry(
            0.35,
            32,
            32
        );

    const material =
        new THREE.MeshBasicMaterial({
            color: 0x38bdf8
        });

    const apple =
        new THREE.Mesh(
            geometry,
            material
        );

    apple.scale.set(
        1,
        0.85,
        0.25
    );

    group.add(apple);


    const glow =
        new THREE.PointLight(
            0x38bdf8,
            2,
            3
        );

    group.add(glow);

    return group;
}


// -----------------------------------------------------
// SNOW LEOPARD SYMBOL
// -----------------------------------------------------

function createLeopard() {

    const group = new THREE.Group();

    const geometry =
        new THREE.IcosahedronGeometry(
            0.35,
            1
        );

    const leopard =
        new THREE.Mesh(
            geometry,
            neonMaterial
        );

    leopard.scale.set(
        1.2,
        0.8,
        0.25
    );

    group.add(leopard);


    return group;
}


// -----------------------------------------------------
// TRACK
// -----------------------------------------------------

function createTrack() {

    const group = new THREE.Group();


    const trackMaterial =
        new THREE.MeshStandardMaterial({
            color: 0x334155,

            metalness: 0.9,

            roughness: 0.3
        });


    for (let z of [-0.7, 0.7]) {

        const railGeometry =
            new THREE.BoxGeometry(
                12,
                0.12,
                0.12
            );

        const rail =
            new THREE.Mesh(
                railGeometry,
                trackMaterial
            );

        rail.position.set(
            0,
            0.2,
            z
        );

        group.add(rail);
    }


    const platformGeometry =
        new THREE.BoxGeometry(
            13,
            0.2,
            4
        );

    const platform =
        new THREE.Mesh(
            platformGeometry,
            darkMaterial
        );

    platform.position.y = 0;

    group.add(platform);


    return group;
}


// -----------------------------------------------------
// MOUNTAINS
// -----------------------------------------------------

function createMountains() {

    const group = new THREE.Group();


    const mountainMaterial =
        new THREE.MeshStandardMaterial({
            color: 0x1e293b,

            roughness: 1
        });


    for (let i = -8; i <= 8; i += 2) {

        const geometry =
            new THREE.ConeGeometry(
                2.5 + Math.random() * 2,
                4 + Math.random() * 4,
                5
            );

        const mountain =
            new THREE.Mesh(
                geometry,
                mountainMaterial
            );

        mountain.position.set(
            i,
            2,
            -10
        );

        mountain.rotation.y =
            Math.random();

        group.add(mountain);
    }

    return group;
}


// -----------------------------------------------------
// STATION
// -----------------------------------------------------

function createStation() {

    const station = new THREE.Group();

    station.name = "station";


    const floorGeometry =
        new THREE.BoxGeometry(
            8,
            0.2,
            5
        );

    const floor =
        new THREE.Mesh(
            floorGeometry,
            darkMaterial
        );

    floor.position.y = 0.2;

    station.add(floor);


    // Columns

    for (let x of [-3, 0, 3]) {

        const columnGeometry =
            new THREE.CylinderGeometry(
                0.12,
                0.12,
                4,
                16
            );

        const column =
            new THREE.Mesh(
                columnGeometry,
                glassMaterial
            );

        column.position.set(
            x,
            2,
            0
        );

        station.add(column);
    }


    // Roof

    const roofGeometry =
        new THREE.BoxGeometry(
            9,
            0.15,
            5
        );

    const roof =
        new THREE.Mesh(
            roofGeometry,
            glassMaterial
        );

    roof.position.y = 4;

    station.add(roof);


    // Turnstiles

    for (let x = -2; x <= 2; x += 1) {

        const turnstileGeometry =
            new THREE.BoxGeometry(
                0.5,
                1,
                0.8
            );

        const turnstile =
            new THREE.Mesh(
                turnstileGeometry,
                neonMaterial
            );

        turnstile.position.set(
            x,
            0.8,
            1
        );

        station.add(turnstile);
    }


    return station;
}


// -----------------------------------------------------
// X-RAY COMMUNICATIONS
// -----------------------------------------------------

function createXRay() {

    const group = new THREE.Group();

    group.name = "xray";


    const roadGeometry =
        new THREE.BoxGeometry(
            12,
            0.2,
            5
        );

    const road =
        new THREE.Mesh(
            roadGeometry,
            darkMaterial
        );

    road.position.y = 0;

    group.add(road);


    const colors = [
        0x38bdf8,
        0x22c55e,
        0xf59e0b,
        0xa855f7
    ];


    for (let i = 0; i < 80; i++) {

        const geometry =
            new THREE.CylinderGeometry(
                0.04,
                0.04,
                6 + Math.random() * 4,
                8
            );

        const material =
            new THREE.MeshBasicMaterial({
                color:
                    colors[
                        Math.floor(
                            Math.random() *
                            colors.length
                        )
                    ]
            });


        const pipe =
            new THREE.Mesh(
                geometry,
                material
            );

        pipe.rotation.z =
            Math.PI / 2;

        pipe.rotation.y =
            Math.random() * Math.PI;

        pipe.position.set(
            (Math.random() - 0.5) * 11,
            0.4 +
                Math.random() * 2.5,
            (Math.random() - 0.5) * 4
        );

        group.add(pipe);
    }


    return group;
}


// -----------------------------------------------------
// CREATE OBJECTS
// -----------------------------------------------------

const train = createTrain();

const track = createTrack();

const mountains = createMountains();

const station = createStation();

const xray = createXRay();


scene.add(
    train,
    track,
    mountains,
    station,
    xray
);


// -----------------------------------------------------
// INITIAL VISIBILITY
// -----------------------------------------------------

station.visible = false;

xray.visible = false;


// -----------------------------------------------------
// VIEW SWITCHING
// -----------------------------------------------------

const buttons =
    document.querySelectorAll(".view-btn");


buttons.forEach(button => {

    button.addEventListener(
        "click",
        () => {

            buttons.forEach(btn =>
                btn.classList.remove("active")
            );

            button.classList.add("active");


            const view =
                button.dataset.view;


            train.visible =
                view === "train";

            track.visible =
                view === "train";


            station.visible =
                view === "station";


            xray.visible =
                view === "xray";


            if (view === "train") {

                camera.position.set(
                    7,
                    4,
                    9
                );

                controls.target.set(
                    0,
                    1.3,
                    0
                );

            }


            if (view === "station") {

                camera.position.set(
                    8,
                    5,
                    9
                );

                controls.target.set(
                    0,
                    1.5,
                    0
                );

            }


            if (view === "xray") {

                camera.position.set(
                    8,
                    6,
                    10
                );

                controls.target.set(
                    0,
                    1,
                    0
                );
            }

        }
    );

});


// -----------------------------------------------------
// ANIMATION
// -----------------------------------------------------

function animate() {

    requestAnimationFrame(animate);

    controls.update();


    // Very subtle train animation

    if (train.visible) {

        train.position.y =
            Math.sin(
                Date.now() * 0.001
            ) * 0.015;

    }


    renderer.render(
        scene,
        camera
    );
}


animate();


// -----------------------------------------------------
// RESIZE
// -----------------------------------------------------

window.addEventListener(
    "resize",
    () => {

        camera.aspect =
            container.clientWidth /
            container.clientHeight;

        camera.updateProjectionMatrix();


        renderer.setSize(
            container.clientWidth,
            container.clientHeight
        );

    }
);
```
