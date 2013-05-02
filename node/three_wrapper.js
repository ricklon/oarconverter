var THREE = require('three');
var scene = new THREE.Scene();
var fs = require('fs');
var data = JSON.parse(fs.readFileSync('./test.out'));
var scene = new THREE.Scene();
var exporter = require('./SceneExporter');
var count=0;
for(var i=0; i<data.length; i++)
{
	if(data[i].Profileshape=="Square")
	{
		var geo = new THREE.CubeGeometry(data[i].Scale.X, data[i].Scale.Y, data[i].Scale.Z);
		var material = new THREE.MeshBasicMaterial({'color': '0x00ff00' });
		var cube = new THREE.Mesh(geo, material);
		cube.position.x=data[i].GroupPosition.X;
		cube.position.y=data[i].GroupPosition.Y;
		cube.position.z=data[i].GroupPosition.Z;
		scene.add( cube);
		count++;
	}
}
console.log(JSON.stringify(exporter.parse(scene)));
