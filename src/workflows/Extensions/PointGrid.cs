using Bonsai;
using System;
using System.ComponentModel;
using System.Reactive.Linq;
using OpenTK;

[Combinator]
[Description("Generate a regular grid of 2D points.")]
[WorkflowElementCategory(ElementCategory.Source)]
public class PointGrid
{
    public PointGrid()
    {
        ExtentX = 2;
        ExtentY = 2;
    }

    [Description("Specifies the number of grid subdivisions along the x-axis.")]
    public int Width { get; set; }

    [Description("Specifies the number of grid subdivisions along the y-axis.")]
    public int Height { get; set; }

    [Description("Specifies the size of the grid along the y-axis.")]
    public float ExtentX { get; set; }

    [Description("Specifies the size of the grid along the y-axis.")]
    public float ExtentY { get; set; }

    [Description("Specifies the location of the grid center along the x-axis.")]
    public float LocationX { get; set; }

    [Description("Specifies the location of the grid center along the y-axis.")]
    public float LocationY { get; set; }

    public IObservable<Vector2[]> Process()
    {
        return Observable.Defer(() =>
        {
            var x = 0.0;
            var y = 0.0;
            var width = Width;
            var height = Height;
            var extentX = ExtentX;
            var extentY = ExtentY;
            var offsetX = LocationX - ExtentX / 2;
            var offsetY = LocationY - ExtentY / 2;
            var widthStep = 1.0 / (width - 1);
            var heightStep = 1.0 / (height - 1);
            var points = new Vector2[width * height];
            for (int i = 0; i < height; i++)
            {
                for (int j = 0; j < width; j++)
                {
                    points[i * width + j] = new Vector2(
                        (float)x * extentX + offsetX,
                        (float)y * extentY + offsetY);
                    x += widthStep;
                }
                
                x = 0;
                y += heightStep;
            }

            return Observable.Return(points);
        });
    }
}
