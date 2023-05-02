# Joint Symmetry Tool

[English](README.md)

Joint Symmetry Toolは、2つの選択されたジョイント間にシンメトリコンストレイント`symmetryConstraint`を設定するためのシンプルなUIを提供するMaya用のPythonスクリプトです。`create_joint_symmetry_ui.py`スクリプトは、対称軸（X、Y、またはZ）を指定することができるUIを作成し、シンメトリコンストレイントを設定する`create_joint_symmetry.py`スクリプトを呼び出します。

## 環境

- Windows 10
- Maya 2020

## インストール

1. このリポジトリをクローンするか、ZIPファイルをダウンロードします。
2. `create_joint_symmetry_ui.py`と`create_joint_symmetry.py`とをMayaのスクリプト用のディレクトリにコピーします。デフォルトの場所は、Windowsの場合は `C:\Users\<username>\Documents\maya\scripts`、macOSの場合は `/Users/<username>/Library/Preferences/Autodesk/maya/scripts` です。
3. Mayaを開き、スクリプトエディタ（`Windows> General Editors> Script Editor`）を開きます。
4. スクリプトエディタで、`File> Open Script`を選択し、スクリプトを保存したディレクトリに移動します。
5. `create_joint_symmetry_ui.py`を開きます。
6. `File> Save Script to Shelf...`を選択し、スクリプトをシェルフに保存して簡単にアクセスできるようにします。

## 使い方

Joint Symmetry Toolを使用するには、以下の手順に従ってください。

1. Joint Symmetry Toolを登録したシェルフのボタンをクリックしてUIを開きます。
2. シンメトリコンストレイントを設定したい2つのジョイントを選択します。最初に選択したジョイントはソースジョイントに、2番目に選択したジョイントはターゲットジョイントになります。
3. 対称軸（X、Y、またはZ）を選択します。
4. `Set Up Symmetry Constraint`ボタンをクリックします。

成功すると、スクリプトは2つの選択したジョイント間にシンメトリコンストレイントノードを作成し、オフセットのために必要なアトリビュートをターゲットジョイントに設定します。エラーが発生した場合、Mayaスクリプトエディタに警告が表示されます。

## ライセンス

このプロジェクトは、MITライセンスの下で公開されています。詳細については[LICENSE](LICENSE)ファイルを参照してください。
