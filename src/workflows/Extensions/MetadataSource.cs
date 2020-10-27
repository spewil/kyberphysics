using Bonsai;
using System;
using System.ComponentModel;
using System.Collections.Generic;
using System.Linq;
using System.Reactive.Linq;

public class Metadata{
    public String name; 
    public int age;
}

[Combinator]
[Description("")]
[WorkflowElementCategory(ElementCategory.Source)]
public class MetadataSource
{
    public String Name{get; set;}
    public int Age{get;set;}
    public IObservable<Metadata> Process()
    {
        var Metadata = new Metadata()
        {
            name = Name, age = Age 
        };
        return Observable.Return(Metadata);
    }
}
