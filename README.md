# Blender Screen Capture

![Screen](./screen.png)

Blenderのウィンドウをキャプチャして画像に反映します。  
VR機能使用時に手元が全くわからないと不便なので作成しました。  
速度上の問題でキャプチャ解像度は 256 * 256 に制限されています。

## usage

- 3D View > その他 > ScreenCapture > start / end で開始・終了する。
- start すると `ScreenCapture` という画像が生成され、リアルタイムにアップデートされる。
- 自分でPlaneを作成しマテリアルを割り当て、シーンに配置する。カメラの子にすると便利。

