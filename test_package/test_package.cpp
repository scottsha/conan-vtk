#include "iostream"

#include <vtkConeSource.h>
#include <vtkPolyData.h>
#include <vtkSmartPointer.h>
#include <vtkPolyDataMapper.h>
#include <vtkActor.h>
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkRenderWindowInteractor.h>

int main(int, char *[])
{
  //Create a cone
  vtkSmartPointer<vtkConeSource> coneSource =
    vtkSmartPointer<vtkConeSource>::New();
  coneSource->Update();
  auto cone = coneSource->GetOutput();
  std::cout << "Cone has " <<cone->GetNumberOfPoints() << " of 7 points." << std::endl;
  return EXIT_SUCCESS;
}
