"use client";
import React from 'react';
import { ShaderGradientCanvas, ShaderGradient } from 'shadergradient';
import * as reactSpring from '@react-spring/three';
import * as drei from '@react-three/drei';
import * as fiber from '@react-three/fiber';

export default function ShaderBackground() {
  return (
    <div className="fixed inset-0 z-0 pointer-events-none opacity-80 mix-blend-screen">
      <ShaderGradientCanvas
        // @ts-ignore
        importedFiber={{ ...fiber, ...drei, ...reactSpring }}
        style={{
          position: 'absolute',
          top: 0,
        }}
        className="w-full h-full"
      >
        <ShaderGradient
          control="query"
          urlString="https://www.shadergradient.co/customize?animate=on&axesHelper=off&bgColor1=%23000000&bgColor2=%23000000&brightness=0.8&cAzimuthAngle=180&cDistance=2.8&cPolarAngle=80&cameraZoom=9.1&color1=%23250b73&color2=%23180429&color3=%230a133f&destination=onCanvas&embedMode=off&envPreset=city&format=gif&fov=45&frameRate=10&gizmoHelper=hide&grain=on&lightType=3d&pixelDensity=1.5&positionX=0&positionY=0.4&positionZ=0&range=disabled&rangeEnd=40&rangeStart=0&reflection=0.1&rotationX=0&rotationY=45&rotationZ=0&shader=defaults&type=waterSphere&uAmplitude=0&uDensity=1.3&uFrequency=0&uSpeed=0.1&uStrength=1.5&uTime=8&wireframe=false"
        />
      </ShaderGradientCanvas>
    </div>
  );
}
