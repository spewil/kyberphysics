using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;
using OpenCV.Net;
using System.Reactive.Concurrency;
​
[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Combinator)]
public class ObserveOnTask
{
    public IObservable<TSource> Process<TSource>(IObservable<TSource> source)
    {
        return source.ObserveOn(Scheduler.TaskPool);
    }
}