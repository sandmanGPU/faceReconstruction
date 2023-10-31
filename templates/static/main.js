// Create a scene
const scene = new THREE.Scene();

// Create a camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// Create a WebGL renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.getElementById('3d-container').appendChild(renderer.domElement);

// Load and display the OBJ model from Cloudflare
const loader = new THREE.OBJLoader();
loader.load('../assests/0.obj', (object) => {
    scene.add(object);
});

// Create controls for easy navigation
const controls = new THREE.OrbitControls(camera, renderer.domElement);

// Create an animation loop
const animate = () => {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
};
animate();