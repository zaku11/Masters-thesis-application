So,
We want to have different class cohesion metrics, which we will calculate for different projects. Basically, a metric is a file that provides us with a function **calculateCohesion**.
The input to this function will be a **ClassInfo** object(see other files for reference), which is roughly a list of methods, members and graph structure of references between them. This should be enough to calculate class cohesion.

To understand class cohesion metrics more please refer to this paper: http://www.math.md/files/csjm/v25-n1/v25-n1-(pp44-74).pdf