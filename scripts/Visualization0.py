import numpy as np
import vtkmodules.vtkInteractionStyle
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkFiltersSources import vtkConeSource, vtkCubeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderer, vtkRenderWindowInteractor
)


def visualization:
    dims=[3, 3, 3]
    dt=1
    len_x=dims[0]
    len_y=dims[1]
    len_z = dims[2]
    n=len_x*len_y*len_z

    #скорости
    v1=np.ones([n], dtype=np.float64)
    v2 = np.ones([n], dtype=np.float64)
    v3 = np.ones([n], dtype=np.float64)

    for i in range(n):
        v1[i]=0.3
        v2[i] = 0.3
        v3[i] = 0.3
    v1[0]=9
    v2[0]=-7
    v3[0]=-1

    conRadius=0.02
    sphereRadius=0.06
    color_begin=(0.0, 0.0, 1.0)
    color_next = (1.0, 0.0, 0.0)
    color_if_big_velocity=(1.0, 1.0, 1.0)
    color_background=(0.5, 0.5, 1)
    color_cones=(1, 0, 1)
    picture_size_x=900
    picture_size_y = 900
    title="Dislocations"
    turn_next_points=True

    # создаём экземпляр vtkConeSource, эти экземпляры могут обрабатывать фильтры
    sphere = vtkSphereSource()
    sphere.SetRadius(sphereRadius)

    con=[0]*n
    for i in range(n):
        con[i]=vtkConeSource()
        con[i].SetRadius(conRadius)

    # создаем экземпляр vtkPolyDataMapper для отображения полигональных данных в графические примитивы
    sphereMapper = vtkPolyDataMapper()
    sphereMapper.SetInputConnection(sphere.GetOutputPort())

    conMapper=[0]*n
    for i in range(n):
        conMapper[i]=vtkPolyDataMapper()
        conMapper[i].SetInputConnection(con[i].GetOutputPort())

    #задаём некоторые общие свойства
    property1 = vtkProperty()
    property1.SetColor(color_begin)
    property1.SetDiffuse(0.7)
    property1.SetSpecular(0.4)
    property1.SetSpecularPower(20)

    property2 = vtkProperty()
    property2.SetColor(color_next)
    property2.SetDiffuse(0.7)
    property2.SetSpecular(0.4)
    property2.SetSpecularPower(20)
    
    property3 = vtkProperty()
    property3.SetColor(color_cones)
    property3.SetDiffuse(0.7)
    property3.SetSpecular(0.4)
    property3.SetSpecularPower(20)

    #создание моделей конусов и шаров
    sphereActor1=[0]*n
    sphereActor2 = [0] * n
    conActor = [0] * n
    for i in range(dims[0]):
        for j in range(dims[1]):
            for z in range(dims[2]):
                sphereActor1[9*i+3*j+z] = vtkActor()
                sphereActor1[9*i+3*j+z].SetMapper(sphereMapper)
                sphereActor1[9*i+3*j+z].SetProperty(property1)
                sphereActor1[9*i+3*j+z].SetPosition(i, j, z)

                sphereActor2[9 * i + 3 * j + z] = vtkActor()
                sphereActor2[9 * i + 3 * j + z].SetMapper(sphereMapper)
                sphereActor2[9 * i + 3 * j + z].SetProperty(property2)
                sphereActor2[9 * i + 3 * j + z].SetPosition(i + v1[9 * i + 3 * j + z] * dt,
                                                            j + v2[9 * i + 3 * j + z] * dt,
                                                            z + v3[9 * i + 3 * j + z] * dt)
                if (v1[9 * i + 3 * j + z] ** 2 + v2[9 * i + 3 * j + z] ** 2 + v3[9 * i + 3 * j + z] ** 2 > 1):
                    sphereActor2[9 * i + 3 * j + z].GetProperty().SetColor(color_if_big_velocity)

                con[9 * i + 3 * j + z].SetHeight(((v1[9 * i + 3 * j + z] ** 2 + v2[9 * i + 3 * j + z] ** 2 + v3[
                    9 * i + 3 * j + z] ** 2) ** 0.5)*dt - 2 * sphereRadius)
                con[9 * i + 3 * j + z].SetDirection(v1[9 * i + 3 * j + z], v2[9 * i + 3 * j + z], v3[9 * i + 3 * j + z])
                conMapper[9 * i + 3 * j + z].SetInputConnection(con[9 * i + 3 * j + z].GetOutputPort())

                conActor[9 * i + 3 * j + z] = vtkActor()
                conActor[9 * i + 3 * j + z].SetMapper(conMapper[9 * i + 3 * j + z])
                conActor[9 * i + 3 * j + z].SetProperty(property3)
                conActor[9 * i + 3 * j + z].SetPosition(i + v1[9 * i + 3 * j + z]*dt / 2, j + v2[9 * i + 3 * j + z]*dt / 2,
                                                        z + v3[9 * i + 3 * j + z]*dt / 2)

    ren1 = vtkRenderer()
    #добавление моделей на изображение
    for i in sphereActor1:
        ren1.AddActor(i)
    if turn_next_points:
        for i in sphereActor2:
            ren1.AddActor(i)
    for i in conActor:
        ren1.AddActor(i)
    ren1.SetBackground(color_background)

    renWin = vtkRenderWindow()
    renWin.AddRenderer(ren1)
    renWin.SetSize(picture_size_x, picture_size_y)
    renWin.SetWindowName(title)

    #подключение камеры
    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    camera = ren1.GetActiveCamera()
    camera.SetViewUp(0, 0, 1)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetPosition(4.5, 4.5, 2.5)
    ren1.ResetCamera()
    camera.Dolly(1.0)
    ren1.ResetCameraClippingRange()

    renWin.Render()
    iren.Start()

if __name__ == '__main__':
    visualization
