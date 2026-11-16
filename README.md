# ComfyUI-luori-Krea2

## 许可证与版权

本仓库自 **2026-11-17** 起采用 **GPL-3.0-or-later**，并适用 `NOTICE`
中依 GPL 第 7 条 (b)(c)(d) 附加的署名保留、来源标注与禁止冒名条款。
此前版本为 **Apache-2.0**；依 Apache-2.0 第 2 条，该授权永久且不可撤销，
历史版本及其快照继续适用原条款。

本仓库全部材料（含 `part/` 下全部 JSON 词库、`示例工作流.json`、源码与文档）
均为 **luori668 私人所有**，不存在其他第三方素材来源或共同权利人。
再分发时须随附 `LICENSE` 与 `NOTICE`，保留作者署名，
并显著标注修改与日期。


一个专为 **Krea2**模型文生图的 ComfyUI 自定义节点插件。

让 Krea2 在 ComfyUI 中使用更方便、更强大，支持更好的提示词处理。


## ✨ 使用方法
comfyUI画布内 双击搜索 落日或者Krea2  即可


## ✨ 主要功能

- 支持 Krea2 提示词的快速抽取（预设超百万字符）
 
## 📦 安装方法

### 方法一：使用 ComfyUI Manager（推荐）
1. 在 ComfyUI 中打开 **Manager**
2. 点击 **Install Custom Nodes**
3. 搜索 `ComfyUI-luori-Krea2`
4. 安装后重启 ComfyUI
 
5.<img width="1637" height="945" alt="03ebd05f-2cbe-4afa-9fe6-00c668d87139" src="https://github.com/user-attachments/assets/058c0e48-183f-4fcc-be0d-a9f8ddfa5914" />







### 方法二：手动安装
```bash
cd ComfyUI/custom_nodes
https://github.com/luori668/ComfyUI-luori-Krea2.git
cd ComfyUI-luori-Krea2
pip install -r requirements.txt

