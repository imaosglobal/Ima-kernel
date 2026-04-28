module.exports = function injectHuman(scene, THREE) {

  const body = new THREE.Group();

  // head
  const head = new THREE.Mesh(
    new THREE.SphereGeometry(0.45, 32, 32),
    new THREE.MeshStandardMaterial({ color: 0x8fd3ff })
  );
  head.position.y = 1.7;

  // eyes (simple but "face exists")
  const eyeGeo = new THREE.SphereGeometry(0.08, 16, 16);
  const eyeMat = new THREE.MeshStandardMaterial({ color: 0x000000 });

  const eyeL = new THREE.Mesh(eyeGeo, eyeMat);
  eyeL.position.set(-0.15, 1.75, 0.35);

  const eyeR = new THREE.Mesh(eyeGeo, eyeMat);
  eyeR.position.set(0.15, 1.75, 0.35);

  // torso
  const torso = new THREE.Mesh(
    new THREE.CylinderGeometry(0.55, 0.75, 1.4, 32),
    new THREE.MeshStandardMaterial({ color: 0x2f7fff })
  );
  torso.position.y = 0.5;

  // arms
  const armGeo = new THREE.CylinderGeometry(0.12, 0.12, 1.2, 16);
  const armMat = new THREE.MeshStandardMaterial({ color: 0x7ec8ff });

  const leftArm = new THREE.Mesh(armGeo, armMat);
  leftArm.position.set(-0.9, 0.6, 0);

  const rightArm = new THREE.Mesh(armGeo, armMat);
  rightArm.position.set(0.9, 0.6, 0);

  // legs
  const legGeo = new THREE.CylinderGeometry(0.15, 0.15, 1.3, 16);

  const leftLeg = new THREE.Mesh(legGeo, armMat);
  leftLeg.position.set(-0.3, -0.9, 0);

  const rightLeg = new THREE.Mesh(legGeo, armMat);
  rightLeg.position.set(0.3, -0.9, 0);

  body.add(head, eyeL, eyeR, torso, leftArm, rightArm, leftLeg, rightLeg);

  scene.add(body);

  return body;
}
