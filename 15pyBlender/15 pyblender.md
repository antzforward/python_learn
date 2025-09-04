---

### **Blender Python API 学习路径**

**核心学习理念：** **“所见即所编”**。每一个代码示例都立即在 Blender 的 3D 视图中看到效果，从而获得即时反馈。

---

#### **第一部分：基础入门**

##### **第 1 章：环境搭建与“Hello, Blender!”**
*   **学习目标：** 了解脚本运行环境，编写并执行第一行代码。
*   **核心内容：**
    *   认识 Blender 的脚本工作区（Scripting Workspace）。
    *   使用 `bpy` 模块和 `bpy.context`（上下文）。
    *   `print(“Hello, Blender!”)` 并在系统控制台查看输出。
*   **示例代码：**
    ```python
    import bpy
    print("我的第一个Blender脚本！")
    print("当前选中的物体是：", bpy.context.object)
    ```
*   **习题：**
    1.  在脚本编辑器中运行示例代码。
    2.  修改代码，打印出你的名字和当前日期。

##### **第 2 章：数据的基石 - 数据块（Datablocks）**
*   **学习目标：** 理解 Blender 数据结构的核心概念。
*   **核心内容：**
    *   什么是数据块（`bpy.types.ID`）？它们共享 `name`、`users` 等属性。
    *   常见数据块类型：`Object`, `Mesh`, `Material`, `Collection`。
    *   学习使用 `bpy.data` 来访问所有数据。
*   **示例代码：**
    ```python
    # 遍历所有物体数据块并打印它们的名字
    for obj in bpy.data.objects:
        print(obj.name)

    # 遍历所有材质数据块
    for mat in bpy.data.materials:
        print(mat.name)
    ```
*   **习题：**
    1.  编写一个脚本，打印出当前场景中所有网格（Meshes）的名字。
    2.  创建一个新的材质数据块，并将其命名为 “My_Red_Material”。

---

#### **第二部分：核心操作**

##### **第 3 章：创建与删除基础物体**
*   **学习目标：** 掌握创建和删除物体的基本命令。
*   **核心内容：**
    *   使用 `bpy.ops` 模块，特别是 `mesh.primitive_*_add` 操作。
    *   理解操作函数的参数（如 `location`, `rotation`, `scale`）。
    *   使用 `bpy.data.objects.remove()` 来删除物体。
*   **示例代码：**
    ```python
    # 在场景原点创建一个立方体
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    # 在 (x=5, y=0, z=0) 的位置创建一个猴头（Suzanne）
    bpy.ops.mesh.primitive_monkey_add(location=(5, 0, 0))
    ```
*   **习题：**
    1.  在场景中创建三个不同位置、不同大小的球体。
    2.  编写一个脚本，先创建一个圆环，然后立即将其删除。

##### **第 4 章：操纵物体 - 变换（Transform）**
*   **学习目标：** 学习如何控制物体的位置、旋转和缩放。
*   **核心内容：**
    *   访问物体的 `location`, `rotation_euler`, `scale` 属性。
    *   直接赋值 vs 使用 `bpy.ops.transform`。
    *   理解局部坐标 vs 全局坐标。
*   **示例代码：**
    ```python
    # 获取当前选中的物体
    my_obj = bpy.context.object

    # 移动它
    my_obj.location.x += 3.0
    my_obj.location = (1, 2, 3) # 直接设置绝对坐标

    # 旋转它 (注意：Blender默认使用弧度制)
    my_obj.rotation_euler = (0, 0, 45 * 3.1416 / 180) # 绕Z轴旋转45度

    # 缩放它
    my_obj.scale = (2, 2, 2) # 在所有维度上放大两倍
    ```
*   **习题：**
    1.  创建一个立方体，并将其绕 Y 轴旋转 90 度，再将其在 X 方向上放大 3 倍。
    2.  （挑战）让一个物体沿着一个圆形路径运动（提示：使用 `sin` 和 `cos` 函数）。

##### **第 5 章：选择与上下文（Context）**
*   **学习目标：** 掌握如何通过代码选择和激活物体，理解上下文的重要性。
*   **核心内容：**
    *   `bpy.context.selected_objects`
    *   `bpy.context.view_layer.objects.active`（激活物体）
    *   使用 `select_set(True/False)` 方法选择/取消选择物体。
    *   许多 `bpy.ops` 操作依赖于当前的选择和激活状态。
*   **示例代码：**
    ```python
    # 取消选择所有物体
    bpy.ops.object.select_all(action='DESELECT')

    # 通过名字获取一个物体
    obj = bpy.data.objects[“Cube”]

    # 选择并激活它
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    ```
*   **习题：**
    1.  编写一个脚本，选择场景中所有名字包含 “Sphere” 的物体。
    2.  创建一个新物体，但不让它成为当前选中的物体。

---

#### **第三部分：进阶建模与修改器**

##### **第 6 章：编辑模式与网格操作**
*   **学习目标：** 进入编辑模式，操作顶点、边和面。
*   **核心内容：**
    *   模式切换：`bpy.ops.object.mode_set(mode=‘EDIT’/’OBJECT’)`。
    *   访问网格数据：`bpy.context.active_object.data`。
    *   遍历 `vertices`, `edges`, `polygons`。
*   **示例代码：**
    ```python
    # 确保在物体模式
    bpy.ops.object.mode_set(mode='OBJECT')

    obj = bpy.context.active_object
    mesh = obj.data

    # 打印第一个顶点的坐标
    print(mesh.vertices[0].co)
    ```
*   **习题：**
    1.  创建一个网格，进入编辑模式，然后通过脚本返回物体模式。
    2.  遍历一个立方体的所有顶点，并打印出它们的全局坐标（提示：使用物体的矩阵世界 `obj.matrix_world`）。

##### **第 7 章：使用修改器（Modifiers）**
*   **学习目标：** 学会以编程方式添加和应用修改器。
*   **核心内容：**
    *   使用 `object.modifiers.new()` 添加修改器。
    *   配置修改器属性（如 `subdivision_levels`， `strength`）。
    *   使用 `bpy.ops.object.modifier_apply()` 应用修改器。
*   **示例代码：**
    ```python
    obj = bpy.context.object

    # 添加表面细分修改器
    mod_subsurf = obj.modifiers.new(name="My Subdivision", type='SUBSURF')
    mod_subsurf.levels = 2

    # 添加倒角修改器
    mod_bevel = obj.modifiers.new(name="My Bevel", type='BEVEL')
    mod_bevel.width = 0.1
    ```
*   **习题：**
    1.  为一个立方体同时添加阵列（Array）和倒角（Bevel）修改器。
    2.  （挑战）编写一个脚本，遍历所有选中的物体，并为它们都添加一个实体化（Solidify）修改器。

---

#### **第四部分：材质、灯光与渲染**

##### **第 8 章：创建并分配材质**
*   **学习目标：** 学习创建材质节点并将其赋予给物体。
*   **核心内容：**
    *   创建材质数据块 `bpy.data.materials.new()`。
    *   启用 `use_nodes`。
    *   访问 `material.node_tree` 和 `material.node_tree.nodes`。
    *   连接节点（`node_tree.links.new`）。
*   **示例代码：**
    ```python
    # 创建新材质并启用节点
    mat = bpy.data.materials.new(name="Red_Glow")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    # 清空默认节点
    nodes.clear()

    # 添加一个漫射BSDF节点和一个输出节点
    bsdf = nodes.new(type='ShaderNodeBsdfDiffuse')
    bsdf.inputs['Color'].default_value = (1, 0, 0, 1) # RGBA: 红色

    output = nodes.new(type='ShaderNodeOutputMaterial')

    # 连接两个节点
    links = mat.node_tree.links
    links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

    # 将材质赋给活动物体
    bpy.context.object.data.materials.append(mat)
    ```
*   **习题：**
    1.  创建一个发光的自发光（Emission）材质，并将其赋给一个球体。
    2.  修改上面的示例，创建一个蓝绿渐变的材质（提示：使用 `ShaderNodeRGB` 和 `ShaderNodeBsdfPrincipled`）。

##### **第 9 章：设置灯光与相机**
*   **学习目标：** 以编程方式创建和配置灯光与相机。
*   **核心内容：**
    *   创建点光、日光、聚光灯：`bpy.ops.object.light_add()`。
    *   创建相机：`bpy.ops.object.camera_add()`。
    *   设置灯光能量（`energy`）、颜色（`color`）。
    *   设置相机焦距（`lens`）和指向目标。
*   **示例代码：**
    ```python
    # 添加一个点光
    bpy.ops.object.light_add(type='POINT', location=(5, 5, 5))
    point_light = bpy.context.object
    point_light.data.energy = 500.0
    point_light.data.color = (1, 0.5, 0.5) # 偏粉色

    # 添加一个相机并指向原点
    bpy.ops.object.camera_add(location=(10, -10, 5))
    camera = bpy.context.object
    # 让相机看向原点 (0,0,0)
    direction = -camera.location
    camera.rotation_euler = direction.to_track_quat(‘-Z’, ‘Y’).to_euler()
    ```
*   **习题：**
    1.  设置一个三点的照明系统（主光、补光、背光）。
    2.  创建一个相机动画，让其环绕一个物体飞行。

##### **第 10 章：渲染输出**
*   **学习目标：** 学会配置渲染引擎并执行渲染。
*   **核心内容：**
    *   设置渲染引擎（`Cycles` 或 `EEVEE`）：`bpy.context.scene.render.engine`。
    *   设置样本数、分辨率等渲染属性。
    *   使用 `bpy.ops.render.render()` 渲染图像和动画。
    *   使用 `bpy.context.scene.render.filepath` 设置输出路径。
*   **示例代码：**
    ```python
    # 设置渲染引擎为Cycles
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 128 # 设置样本数

    # 设置输出分辨率为1920x1080
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080

    # 设置输出文件格式为PNG
    bpy.context.scene.render.image_settings.file_format = 'PNG'

    # 设置输出路径并渲染单张图片
    bpy.context.scene.render.filepath = “//my_render.png”
    bpy.ops.render.render(write_still=True) # 渲染并保存
    ```
*   **习题：**
    1.  编写一个脚本，将渲染引擎切换为 EEVEE，并设置环境光遮蔽（Ambient Occlusion）为开启。
    2.  渲染一个 500x500 像素的图片，并将其保存到你的桌面。

---

#### **第五部分：综合应用与自动化**

##### **第 11 章：制作关键帧动画**
*   **学习目标：** 学习如何通过代码插入关键帧，制作动画。
*   **核心内容：**
    *   使用 `object.keyframe_insert(data_path, frame)`。
    *   为位置、旋转、缩放甚至材质属性设置关键帧。
*   **示例代码：**
    ```python
    obj = bpy.context.object
    scene = bpy.context.scene

    # 在第1帧，设置物体的初始位置
    scene.frame_set(1)
    obj.location.x = 0
    obj.keyframe_insert(data_path=“location”, index=0) # index=0 代表X轴

    # 在第24帧，改变位置并设置另一个关键帧
    scene.frame_set(24)
    obj.location.x = 5
    obj.keyframe_insert(data_path=“location”, index=0)
    ```
*   **习题：**
    1.  让一个物体在 50 帧内完成一次完整的旋转。
    2.  让一个物体的材质颜色从红色随时间变化（50帧）为蓝色。

##### **第 12 章：创建自定义运算符（Operator）**
*   **学习目标：** 将你的脚本封装成可以在 Blender 界面中点击执行的工具。
*   **核心内容：**
    *   定义一个继承自 `bpy.types.Operator` 的类。
    *   设置 `bl_idname`, `bl_label`, `bl_options`。
    *   实现 `execute(self, context)` 方法。
    *   注册（register）和取消注册（unregister）你的类。
*   **示例代码：**
    ```python
    import bpy

    class MESH_OT_add_my_special_cube(bpy.types.Operator):
        """我的工具提示：添加一个特殊的立方体""" 
        bl_idname = “mesh.add_my_special_cube”
        bl_label = “添加特殊立方体”
        bl_options = {‘REGISTER’, ‘UNDO’}

        def execute(self, context):
            bpy.ops.mesh.primitive_cube_add()
            new_cube = context.object
            new_cube.scale = (1, 1, 3) # 让它变得高一些
            self.report({'INFO’}, “一个特殊的立方体被创建了！”)
            return {'FINISHED’}

    # 注册
    def register():
        bpy.utils.register_class(MESH_OT_add_my_special_cube)

    # 取消注册
    def unregister():
        bpy.utils.unregister_class(MESH_OT_add_my_special_cube)

    if __name__ == “__main__”:
        register()
    ```
*   **习题：**
    1.  将上一章创建的动画脚本改造成一个操作符，点击后自动为选中的物体创建动画。
    2.  在 F3 搜索菜单中查找你自定义的操作符并运行它。

##### **第 13 章：综合项目**
*   **学习目标：** 综合运用所学知识，完成一个完整项目。
*   **项目建议：**
    1.  **程序化生成城市：** 编写一个脚本，在网格上随机生成不同高度和颜色的立方体来模拟建筑。
    2.  **材质分发器：** 创建一个工具，为场景中所有选中的物体随机分配一个预设材质库中的材质。
    3.  **场景组装器：** 从一个文本文件（如CSV）中读取数据（位置、物体类型、颜色），并自动在 Blender 中生成整个场景。

---

#### **高级主题学习路径（续接基础之后）**

##### **第 14 章：深入材质与着色器 (Shader) 编程**
*   **学习目标：** 超越基础 Principled BSDF，动态创建和修改复杂的节点材质。
*   **核心内容：**
    *   深入 `bpy.data.materials['name'].node_tree`：访问、遍历、创建和连接节点 (`nodes.new`, `links.new`)。
    *   熟悉常用 `ShaderNode` 类型（如 `ShaderNodeEmission`（发光）, `ShaderNodeTexImage`（图像纹理）, `ShaderNodeRGB`（RGB节点）等）及其输入输出接口。
    *   动态修改着色器属性（如颜色、强度），并为材质属性添加**驱动（Driver）**或**关键帧（Keyframe）**以实现动画效果。
*   **示例代码（创建发光材质）：**
    ```python
    import bpy

    def create_emission_shader(color, strength, mat_name):
        # 创建新材质并启用节点
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        # 清空默认节点
        nodes.clear()

        # 创建发光节点
        node_emission = nodes.new(type='ShaderNodeEmission')
        node_emission.inputs[0].default_value = color  # 颜色 (RGBA)
        node_emission.inputs[1].default_value = strength  # 强度
        node_emission.location = (0, 0)

        # 创建材质输出节点
        node_output = nodes.new(type='ShaderNodeOutputMaterial')
        node_output.location = (200, 0)

        # 连接节点
        links = mat.node_tree.links
        links.new(node_emission.outputs[0], node_output.inputs[0])

        return mat

    # 使用函数创建一个黄色的自发光材质
    yellow_glow = create_emission_shader((1, 0.8, 0, 1), 10.0, "Yellow_Glow_Mat")
    # 赋给当前选中的物体
    if bpy.context.object:
        bpy.context.object.data.materials.append(yellow_glow)
    ```
*   **习题：**
    1.  编写一个脚本，创建一个新的材质，其中包含一个 `ShaderNodeRGB` 节点并将其颜色输出到 `Principled BSDF` 的 `Base Color` 输入。
    2.  （挑战）为你创建的发光材质的强度属性添加一个驱动，使其随着物体的位置变化而变化。

##### **第 15 章：操作几何节点 (Geometry Nodes)**
*   **学习目标：** 用 Python 创建、分配和修改几何节点修改器，实现程序化建模。
*   **核心内容：**
    *   理解几何节点组 (`bpy.data.node_groups`) 也是一种数据块。
    *   使用 `bpy.ops.object.modifier_add` 添加几何节点修改器并指定节点组。
    *   **(高级)** 使用 Python 创建和构建一个完整的几何节点组（创建节点组、添加输入输出节点、内部节点并连接）。
*   **示例代码（为物体添加现有几何节点组）：**
    ```python
    import bpy

    # 假设我们有一个名为 "My_Geometry_Nodes" 的节点组
    geo_nodes_name = "My_Geometry_Nodes"
    obj = bpy.context.object

    if obj:
        # 添加几何节点修改器
        modifier = obj.modifiers.new(name="MyGeoNodes", type='NODES')
        # 尝试获取已有的节点组并赋值给修改器
        if geo_nodes_name in bpy.data.node_groups:
            modifier.node_group = bpy.data.node_groups[geo_nodes_name]
        else:
            print(f"警告：未找到名为 '{geo_nodes_name}' 的几何节点组！")
            # 你也可以选择在这里用 bpy.data.node_groups.new(geo_nodes_name, 'GeometryNodeTree') 创建一个新的
    ```
*   **习题：**
    1.  手动创建一个简单的几何节点组（例如，分散一些实例在立方体上）。编写脚本，将这个节点组应用到一个新物体的修改器上。
    2.  （高级挑战）尝试用 Python 脚本创建一个全新的几何节点组，包含一个“网格立方体”节点和一个“实例化于点上”节点，并使用“分布点于体积上”节点来提供点。

##### **第 16 章：动画与关键帧**
*   **学习目标：** 使用 Python 精确控制动画，为各种属性插入关键帧。
*   **核心内容：**
    *   使用 `keyframe_insert(data_path, frame)` 方法为任何属性的变化插入关键帧。
    *   理解 `data_path`（如 `location`, `rotation_euler`, `scale`, `data.materials[0].node_tree.nodes["Principled BSDF"].inputs[0].default_value`）。
    *   使用 `driver_add` 和 `driver_remove` 为属性创建和移除驱动表达式。
*   **示例代码（让物体跳跃）：**
    ```python
    import bpy

    obj = bpy.context.object
    if obj:
        start_frame = 1
        obj.location.z = 0
        # 在第1帧为Z位置插入关键帧
        obj.keyframe_insert(data_path="location", index=2, frame=start_frame)

        # 到第15帧
        mid_frame = 15
        obj.location.z = 3 # 跳到空中
        obj.keyframe_insert(data_path="location", index=2, frame=mid_frame)

        # 到第30帧
        end_frame = 30
        obj.location.z = 0 # 落回地面
        obj.keyframe_insert(data_path="location", index=2, frame=end_frame)
    ```
*   **习题：**
    1.  让一个物体在 100 帧内绕 Z 轴连续旋转 5 圈，并设置关键帧。
    2.  为一个材质的颜色（RGB节点）制作一个从红到蓝再变绿的颜色变换动画。

##### **第 17 章：特效、模拟与渲染集成**
*   **学习目标：** 了解如何用脚本控制粒子、物理模拟和渲染设置。
*   **核心内容：**
    *   操作粒子系统设置 (`bpy.data.particles`)。
    *   （简介）触发烘焙物理模拟。
    *   **自动化渲染输出**：这是 Python 脚本非常强大的应用领域。你可以批量修改设置（如分辨率、样本数、引擎（Cycles/EEVEE）），遍历多个相机角度或不同材质/贴图的版本，然后自动渲染并保存到指定位置。
*   **示例代码（批量更改贴图并渲染）：**
    ```python
    import bpy
    import os

    # 假设有一个物体和它的材质，材质中有一个图像纹理节点名为 "Image Texture"
    obj_name = "猴头"
    image_texture_node_name = "Image Texture"
    texture_folder = "//textures/"  # Blender 相对路径，指向 blend 文件所在目录的 textures 文件夹
    output_folder = "//renders/"

    # 确保输出目录存在
    os.makedirs(bpy.path.abspath(output_folder), exist_ok=True)

    obj = bpy.data.objects.get(obj_name)
    if obj and obj.data.materials:
        mat = obj.data.materials[0]
        tex_node = mat.node_tree.nodes.get(image_texture_node_name)

        if tex_node and tex_node.image:
            # 获取 textures 文件夹下所有 jpg 文件
            textures = [img for img in os.listdir(bpy.path.abspath(texture_folder)) if img.lower().endswith('.jpg')]
            for tex_name in textures:
                tex_path = os.path.join(texture_folder, tex_name)
                # 更改贴图
                tex_node.image.filepath = tex_path
                # 设置输出路径和文件名
                output_path = os.path.join(output_folder, f"render_{os.path.splitext(tex_name)[0]}.png")
                bpy.context.scene.render.filepath = output_path
                # 执行渲染
                bpy.ops.render.render(write_still=True)
    ```
*   **习题：**
    1.  编写一个脚本，将场景的渲染引擎从 EEVEE 切换到 Cycles，并将渲染样本数设置为 256。
    2.  （项目式）创建一个包含 10 个球的场景，每个球有不同的自发光颜色和强度。编写脚本，从 5 个不同的相机角度渲染这个场景，并将图片保存到不同的文件夹。

---

### **为什么这些高级主题很棒**

用 Python 控制这些方面，意味着你可以：
*   **程序化生成内容**：比如根据规则自动生成建筑、植被或抽象艺术。
*   **批量处理**：一次性渲染数百张图片或视频，无需手动操作，特别适合制作产品目录、多角度展示或测试不同材质效果。
*   **创建动态系统**：让材质属性根据时间、物体位置或其他因素自动变化，创造出非常有机和复杂的效果。
*   **构建自定义工具**：将复杂的节点设置或动画流程打包成一个简单的按钮，大大提高创作效率。

---

**给学习者的最终建议：**

1.  **多查文档：** 遇到不懂的类或属性，按 `F1` 或直接去 [Blender Python API 文档](https://docs.blender.org/api/current/) 搜索。
2.  **善用补全：** 在脚本编辑器中按 `Ctrl+Space` 可以触发代码补全，这是探索 API 的绝佳方式。
3.  **从模仿开始：** 在 Blender 中手动执行一个操作，然后在“信息”窗口（Info Window）查看它记录了哪些 Python 命令。这是反向学习 API 的黄金方法。
4.  **不要害怕犯错：** 代码出错是学习过程的一部分。仔细阅读错误信息，它们通常会告诉你问题出在哪里。
5.   **循序渐进**：确保你已经掌握了前面基础部分（物体操作、数据块、变换等），再冲击这些高级主题。它们是对基础知识的综合应用。
6.   **“模仿”是最好的起点**：在 Blender 界面中手动创建一个你想要的着色器或几何节点效果，然后在 Python 脚本中尝试一步步复现这个过程。**Info 窗口**（Scripting Workspace 里）会显示你手动操作对应的 Python 命令。
7.   **官方文档是终极武器**：遇到不懂的节点类型或属性，随时查阅 [Blender Python API 文档](https://docs.blender.org/api/current/)。按 `F1` 也能快速跳转到当前选中内容的文档。
8. **从小实验开始**：不要一开始就想着做庞大的项目。先成功改变一个颜色，添加一个简单的节点，让一个物体动起来。每一个小成功都会给你正反馈。
