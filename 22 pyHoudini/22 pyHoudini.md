# 22 pyHoudini   
***   
好的，绝对可以。Houdini 的 Python API（以及其传统的 HScript 和 HOM 扩展）是其强大程序化能力的核心。学习它不仅能让你自动化任务，更能让你深入理解 Houdini 的底层架构，从而创造出无限可能。

下面我为你设计一个系统的、从入门到精通的 Houdini Python API 学习课程结构。

---

### **课程总名称：Houdini Python API 精通：从脚本编写到程序化生成大师**

**核心目标**：本课程旨在让你不仅学会调用 Houdini 的 Python API，更要理解其**基于节点（Node-Based）** 和**程序化（Procedural）** 的核心哲学。最终目标是让你能够**通过脚本创建、修改和连接节点**，**动态生成复杂几何体**，**构建自定义工具（Digital Assets）**，并**与外部数据源和流程进行集成**，从而彻底释放 Houdini 的潜力。

---

### **分课程设计与学习目标**

#### **第一部分：基础入门与 Houdini 对象模型（HOM）**

*   **课程 1.1：环境搭建与“Hello Houdini”**
    *   **学习目标**：了解在 Houdini 中运行 Python 脚本的各种方式，理解 `hou` 模块，并成功运行第一个脚本。
    *   **核心内容**：
        *   脚本位置：Python Shell、Python Source Editor（`alt+shift+p`）、节点参数表达式、外部 IDE。
        *   导入 `hou` 模块：`import hou`
        *   使用 `hou.ui` 模块显示消息：`hou.ui.displayMessage("Hello Houdini!")`
        *   获取和设置当前选择的节点。
    *   **关键概念**：`hou` 模块、HOM (Houdini Object Model)。
    *   **习题**：
        1.  在 Python Shell 中打印出你的 Houdini 版本号（`hou.applicationVersionString()`）。
        2.  编写一个脚本，显示一个对话框，内容是当前选择的节点名称（使用 `hou.selectedNodes()`）。

*   **课程 1.2：节点图（Node Graph）与网络（Network）遍历**
    *   **学习目标**：掌握如何通过代码获取、创建、删除和连接节点，理解节点的层级结构。
    *   **核心内容**：
        *   获取当前网络编辑器：`hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)`
        *   获取节点：`hou.node("/obj/geo1")`，`hou.selectedNodes()`，`parentNode.children()`
        *   创建节点：`parentNode.createNode("geo")`， `parentNode.createNode("box")`
        *   连接节点：`node.setInput(0, source_node)`
        *   删除节点：`node.destroy()`
    *   **关键概念**：节点路径（Path）、网络（Network）、父级/子级关系。
    *   **习题**：
        1.  编写一个脚本，在 `/obj` 上下文下自动创建一个 `geo` 节点，并在其内部创建一个 `box` 和一个 `sphere` 节点。
        2.  编写一个脚本，将当前选中的两个节点连接起来（第一个节点连接到第二个节点的第一个输入）。

*   **课程 1.3：参数（Parameters）读写与控制**
    *   **学习目标**：学会获取和设置节点的参数值，这是自动化操作的基础。
    *   **核心内容**：
        *   获取参数：`node.parm("size")`，`node.evalParm("size")`
        *   设置参数：`node.parm("size").set(2.5)`
        *   查找和遍历参数：`node.parms()`，`node.parmTuples()`
        *   理解 `Parm` 和 `ParmTuple` 的区别（如 `t` (tx,ty,tz) 是一个 ParmTuple）。
    *   **关键概念**：参数（Parm）、计算（evalParm 与直接 set 的区别）。
    *   **习题**：
        1.  选中一个 `box` 节点，编写脚本将其 `scale` 参数在 X, Y, Z 方向上分别设置为 1, 2, 3。
        2.  编写一个脚本，随机设置选中节点的 `tx`, `ty`, `tz` 值。

#### **第二部分：几何体（Geometry）的深度操作**

*   **课程 2.1：几何体数据结构（Point, Vertex, Primitive, Detail）**
    *   **学习目标**：理解 Houdini 几何体的核心数据结构和 `hou.Geometry` 对象，这是最核心和强大的部分。
    *   **核心内容**：
        *   从节点获取几何体：`geometry = node.geometry()` （需要在烹饪（Cook）之后）。
        *   遍历和访问元素：
            *   `geometry.points()` （点）
            *   `geometry.prims()` （基元，如多边形）
            *   `geometry.vertices()` （顶点，连接点和基元）
        *   理解 `Detail` 属性（全局属性）。
    *   **关键概念**：点（Point）、顶点（Vertex）、基元（Primitive）、详情（Detail）。
    *   **习题**：
        1.  选中一个 `geo` 节点，编写脚本打印出其内部几何体的点数和面数。
        2.  遍历一个网格的所有点，打印出它们的的位置 `point.position()`。

*   **课程 2.2：属性（Attributes）的读写与创建**
    *   **学习目标**：掌握如何读取和创建几何体属性（如 `P`、`N`、`Cd` 以及自定义属性）。
    *   **核心内容**：
        *   读取属性：`point.attribValue("P")`, `geometry.pointFloatAttribValues("pscale")`
        *   创建和设置属性：
            *   `geometry.addAttrib(hou.attribType.Point, "my_attr", 0.0)`
            *   `point.setAttribValue("my_attr", 1.0)`
        *   理解不同属性类型（Point, Prim, Vertex, Detail）。
    *   **关键概念**：属性（Attribute）、属性类型、数据数组。
    *   **习题**：
        1.  创建一个 `box`，为其每个点添加一个自定义浮点属性 `height`，并根据点的 Y 坐标设置该属性的值。
        2.  读取一个网格的 `Cd`（颜色）属性，并将其所有颜色的红色分量（R）乘以 2。

*   **课程 2.3：通过代码创建几何体**
    *   **学习目标**：学习如何从零开始，通过 Python 代码动态构建几何体，这是程序化生成的核心。
    *   **核心内容**：
        *   创建 `geo` 节点并获取其几何体：`node = hou.node("/obj/geo1")`，`geo = node.geometry()` （需要先清空或创建 `geometry` 对象）。
        *   使用 `Geometry.createPoint()` 创建点。
        *   使用 `Geometry.createPolygon()` 或多边形建造方法（`hou.Polygon`）创建面。
        *   在 `/obj` 上下文中创建 `python` 节点（Geometry Operator）。
    *   **关键概念**：Python SOP（Geometry Operator）。
    *   **习题**：
        1.  在 Python SOP 中编写代码，生成一个由 100 个随机位置的点组成的点云。
        2.  （挑战）在 Python SOP 中编写代码，创建一个参数化的螺旋线几何体。

#### **第三部分：高级应用与集成**

*   **课程 3.1：创建自定义工具（Digital Assets）**
    *   **学习目标**：将你的 Python 脚本封装成可复用的、带界面的自定义节点（HDA）。
    *   **核心内容**：
        *   在 HDA 类型属性中设置 Python 脚本。
        *   在参数回调脚本（Callback Script）中响应用户操作。
        *   使用 `kwargs` 获取当前节点（`node`）和参数（`parm`）等信息。
    *   **关键概念**：HDA (Houdini Digital Asset)、回调脚本（Callback Script）、`kwargs`。
    *   **习题**：
        1.  创建一个 HDA，它有一个按钮（Button parameter），点击后会在场景中生成一个随机位置的立方体。
        2.  创建一个 HDA，它有一个 `radius` 参数，当用户拖动滑块时，通过回调脚本实时更新该节点内一个球体的尺寸。

*   **课程 3.2：事件处理与 UI 定制**
    *   **学习目标**：学习响应 Houdini 的事件（如文件加载、节点创建）并定制用户界面。
    *   **核心内容**：
        *   使用 `hou.session` 模块存储自定义函数和状态。
        *   使用 `hou.hscript()` 执行 HScript 命令（与旧系统交互）。
        *   了解 `hou.hipFile` 事件（如 `onLoad`）。
        *   使用 `hou.ui` 创建自定义浮动面板（Pane Tab）。
    *   **关键概念**：事件回调、HScript 集成、`hou.session`。
    *   **习题**：
        1.  编写一个脚本，在 Houdini 文件打开时自动在 `/obj` 下创建一个备份 `geo` 节点。
        2.  创建一个自定义的浮动面板，上面有一个按钮，可以清理当前场景中未使用的节点。

*   **课程 3.3：外部集成与批量处理**
    *   **学习目标**：让 Houdini 与外部世界交互，实现批量渲染、数据处理等自动化流程。
    *   **核心内容**：
        *   使用 `hou.hipFile.load()` 和 `hou.hipFile.save()` 操作文件。
        *   使用 `hou.render()` 启动渲染，并监控进度。
        *   使用标准 Python 模块（如 `json`, `csv`, `requests`）读写数据。
        *   使用 `hython` 无头（Headless）运行脚本。
    *   **关键概念**：无头渲染、流程集成、`hython`。
    *   **习题**：
        1.  编写一个 `hython` 脚本，打开一个 `.hip` 文件，渲染指定相机，并保存图像，然后退出。
        2.  编写一个脚本，从 `.csv` 文件中读取位置数据，并在 Houdini 中生成对应的点。

---

### **最终大项目：综合实践**

整合所有所学知识，完成以下一项或多项：

1.  **程序化建筑生成器**：创建一个 HDA，通过 Python 脚本控制，根据输入曲线和参数（如楼层数、窗户类型、楼高变化）程序化生成一栋建筑。核心使用 **Python SOP** 来构建几何体，并用 **HDA 参数** 暴露控制项。
2.  **自定义破碎工具**：创建一个比内置破碎更复杂的工具，允许用户绘制破碎图案，或根据贴图来控制破碎强度。核心使用 **节点创建/连接** 来组装节点网络，并用 **属性读写** 来传递数据。
3.  **流程集成工具**：创建一个工具，自动从指定目录扫描模型文件，导入到 Houdini 中，为其分配预设材质，并批量渲染 turntable 动画。核心使用 **外部集成（文件操作）** 和 **批量渲染**。

通过这个由浅入深的结构化学习路径，你将能够系统性地掌握 Houdini Python API，从简单的脚本助手成长为能够开发复杂程序化工具的技术专家。祝你学习愉快！