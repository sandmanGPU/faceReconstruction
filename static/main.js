import * as THREE from 'three';

import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
let currentIndex=0
let camera, scene, renderer;
var objList = [];
let object;

init();


export function init() {

	camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 0.1, 20 );
	camera.position.z = 2.5;

	// scene

	scene = new THREE.Scene();

	const ambientLight = new THREE.AmbientLight( 0xffffff );
	scene.add( ambientLight );

	const pointLight = new THREE.PointLight( 0xffffff, 15 );
	camera.add( pointLight );
	scene.add( camera );

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
		// For example, you can loop through the filenames and perform actions in JavaScript
		// for (var i = 0; i < objList.length; i++) {
		// 	var filename = objList[i];
		// 	{{filename}}
		// 	// Perform actions with each filename
		// }
	});


    // Add event listeners for the "Prev" and "Next" buttons
    document.getElementById('prev-button').addEventListener('click', loadPreviousModel);
    document.getElementById('next-button').addEventListener('click', loadNextModel);

	function loadModel(objURL) {
	// Clear the previous object if there was one
	if (object) {
		scene.remove(object);
	}
    
	const loader = new OBJLoader();
	loader.load(objURL, function (obj) {
		object = obj;
		object.position.y = 0.0;
		object.scale.setScalar(1);
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
	renderer.setSize( window.innerWidth/4, window.innerHeight/4);
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

	camera.aspect = window.innerWidth / window.innerHeight;
	camera.updateProjectionMatrix();

	renderer.setSize( window.innerWidth/4, window.innerHeight/4);
	render()

}

export function render() {

	renderer.render( scene, camera );

}

