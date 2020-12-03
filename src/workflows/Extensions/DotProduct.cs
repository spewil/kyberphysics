using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using OpenCV.Net;

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Transform)]
public class DotProduct
{
    public IObservable<Mat> Process(IObservable<Tuple<Mat, Mat>> source)
    {   
        return source.Select(value => 
        {
            var result = new Mat(value.Item1.Rows,value.Item2.Cols,value.Item1.Depth,value.Item1.Channels);
            CV.GEMM(value.Item1,value.Item2,1,null,1,result);
            return result;

        });
    }
}