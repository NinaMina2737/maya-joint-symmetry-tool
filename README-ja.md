# Maya Joint Symmetry Tool

[English](README.md)

Joint Symmetry Toolは、2つの選択されたジョイント間にシンメトリコンストレイント`symmetryConstraint`を設定するためのシンプルなUIを提供するMaya用のPythonスクリプトです。`create_joint_symmetry_ui.py`スクリプトは、対称軸（X、Y、またはZ）を指定することができるUIを作成し、シンメトリコンストレイントを設定する`create_joint_symmetry.py`スクリプトを呼び出します。

## 環境

- Windows 10
- Maya 2020

## インストール

1. [最新リリース](https://github.com/NinaMina2737/maya-joint-symmetry-tool/releases/latest)をダウンロードし、アーカイブを展開してください。
2. `maya-joint-symmetry-tool`フォルダを Maya のスクリプトフォルダに移動してください。(例: `C:\Users\<user>\Documents\maya\scripts`)
3. `install.py`をMayaのビューポートにドラッグ&ドロップしてください。
4. これで、アクティブなシェルフに`jointSymmetryTool`が追加されます。

## 使い方

Joint Symmetry Toolを使用するには、以下の手順に従ってください。

1. シェルフから`jointSymmetryTool`を実行してください。
2. シンメトリコンストレイントを設定したい2つのジョイントを選択します。最初に選択したジョイントはソースジョイントに、2番目に選択したジョイントはターゲットジョイントになります。
3. 対称軸（X、Y、またはZ）を選択します。
4. `Set Up Symmetry Constraint`ボタンをクリックします。

成功すると、スクリプトは2つの選択したジョイント間にシンメトリコンストレイントノードを作成し、オフセットのために必要なアトリビュートをターゲットジョイントに設定します。エラーが発生した場合、Mayaスクリプトエディタに警告が表示されます。

## ライセンス

このプロジェクトは、MITライセンスの下で公開されています。詳細については[LICENSE](LICENSE)ファイルを参照してください。
