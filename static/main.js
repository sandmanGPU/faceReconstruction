import * as THREE from 'three';

import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
let currentIndex=0
let camera, scene, renderer;
var objList = [];
let object;

init();
export function init() {

	camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.05, 500 );
	camera.position.set(1, 1, 2.5);

	// scene

	scene = new THREE.Scene();
	scene.background = new THREE.Color(0xEAEAEA);
	const gridHelper = new THREE.GridHelper(10, 10); // Parameters: size (total grid size), divisions (number of divisions)
	// scene.add(gridHelper);

	
	const ambientLight = new THREE.AmbientLight( 0xffffff );
	scene.add( ambientLight );

	const pointLight = new THREE.PointLight( 0xffffff, 15 );
	camera.add( pointLight );
	scene.add( camera );

	// Create a spot light
	const spotLight = new THREE.SpotLight(0xffffff); // Set the light color

	// Set the light's position
	spotLight.position.set(10, 10, -10); // Set the position of the spot light

	// Set the direction in which the light is pointing
	spotLight.target.position.set(0, 0, 0); // Set the target position for the light

	// Define the light's properties
	spotLight.distance = 200; // Set the maximum distance over which the light can reach
	spotLight.angle = Math.PI / 6; // Set the angle of the light cone in radians
	spotLight.penumbra = 0.1; // Set the penumbra (softness) of the light's edges

	scene.add(spotLight); // Add the spot light to your scene


	document.addEventListener("DOMContentLoaded", function() {
		// Access the Python list of filenames in JavaScript
		var filenamesElement = document.getElementById('filenames');
	    objList = JSON.parse(filenamesElement.textContent);
	
		// Now, 'filenames' contains the list of filenames, and you can work with it in your JavaScript code.
		console.log(objList);
		if(objList.length > 0){
			loadModel(objList[0]);
			currentIndex=0
		}
	});

	document.getElementById('carouselPrevButton').addEventListener('click', loadPreviousModel);
	document.getElementById('carouselNextButton').addEventListener('click', loadNextModel);


	function loadModel(objURL) {
	// Clear the previous object if there was one
	if (object) {
		scene.remove(object);
	}
    
	const loader = new OBJLoader();
	loader.load(objURL, function (obj) {
		object = obj;
		object.position.y = 0.0;
		var boundingBox = new THREE.Box3().setFromObject(object);
		var center = boundingBox.getCenter(new THREE.Vector3());
		var size = boundingBox.getSize(new THREE.Vector3());
		var maxDim = Math.max(size.x, size.y, size.z);
		var scaleFactor = 1 / maxDim*1.4;


		object.scale.set(scaleFactor, scaleFactor, scaleFactor);
		object.position.sub(center.multiplyScalar(scaleFactor));
		// object.scale.setScalar(1);
		scene.add(object);
		render();
	}, onProgress, onError);
	}

	function loadPreviousModel() {
		console.log(currentIndex);
		if (currentIndex > 0) {
			currentIndex--;
			loadModel(objList[currentIndex]);
		}
	}
	
	
	function loadNextModel() {
		console.log(currentIndex);

		if (currentIndex < objList.length - 1) {
			currentIndex++;
			loadModel(objList[currentIndex]);
		}
	}
	

	const manager = new THREE.LoadingManager( loadModel );

	// texture

	// const textureLoader = new THREE.TextureLoader( manager );
	// const texture = textureLoader.load( 'textures/uv_grid_opengl.jpg', render );
	// texture.colorSpace = THREE.SRGBColorSpace;

	// model

	function onProgress( xhr ) {

		if ( xhr.lengthComputable ) {

			const percentComplete = xhr.loaded / xhr.total * 100;
			console.log( 'model ' + percentComplete.toFixed( 2 ) + '% downloaded' );

		}

	}

	function onError() {}

	const loader = new OBJLoader( manager );
	// loader.load( 'static/public/1.obj', function ( obj ) {

	// 	object = obj;

	// }, onProgress, onError );

	//

	renderer = new THREE.WebGLRenderer( { antialias: true } );
	renderer.setPixelRatio( window.devicePixelRatio );
	renderer.setSize( window.innerWidth/3.5, window.innerHeight/3.5+100);
	camera.aspect = (window.innerWidth/3.5) / (window.innerHeight/3.5+100);
	camera.updateProjectionMatrix();
	document.getElementById('model-container').appendChild( renderer.domElement );
	//
	const controls = new  OrbitControls( camera, renderer.domElement );
	controls.minDistance = 2;
	controls.maxDistance = 5;
	controls.addEventListener( 'change', render );
	//
	window.addEventListener( 'resize', onWindowResize );

}

export function onWindowResize() {

	

	renderer.setSize( window.innerWidth/3.5, window.innerHeight/3.5+100);
	camera.aspect = (window.innerWidth/3.5) / (window.innerHeight/3.5+100);
	camera.updateProjectionMatrix();
	render()

}

export function render() {

	renderer.render( scene, camera );

}

