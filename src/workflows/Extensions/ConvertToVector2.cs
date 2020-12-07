using Bonsai;
using System;
using System.ComponentModel;
using System.Linq;
using System.Reactive.Linq;
using OpenCV.Net;
using OpenTK;

[Combinator]
[Description("Converts a 2x1 or 1x2 matrix into a Vector2.")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class ConvertToVector2
{
    public IObservable<Vector2> Process(IObservable<Mat> source)
    {
        return source.Select(value => new Vector2((float)value.GetReal(0), (float)value.GetReal(1)));
    }
}
