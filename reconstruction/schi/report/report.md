# Architetural reconstruction

## Introduction

<!-- TODO: Introduce symphony approach maybe? -->

## Problem elicitation

When following an education in a computer science relevant field, students will be taught the fundamentals of computers and programming. This involves many topics as it is a complex topic. What an education most of the time does not include---for good reasons, that shall not be argued here, as this is not the focus of the report---is the work with frameworks. Frameworks are a set of reusable libraries for software systems. A popular area of computing where the number of frameworks is countless is for the development of web applications.
These web frameworks have been built most of the time by a single person and then evolved to a code base, so complex that many developers actively maintain and expand it.
Due to the complexity of these frameworks one focus point has been to make the intial set up and usuage as easy as possible, often being able to have a running web application within minutes. This is valuable, but comes with the risk of using the framework without knowing what is actually happening.
Documentation is a key aspect of enabling this bridge from practice to theory and vice versa.
Another part of open-source frameworks is that they rely heavily on the community to chip in, as open-source lives from contributions from everyone. But how does one contribute to a code base that has 394,884 lines of code, increasing by the hour.
Documentation helps here as well, but is harder to maintain, because it would have be updated with every code change, whereas the documentation of the frameworks' functionality only needs updating when a major feature gets added or updated.
This report aims at giving a programmatic overview of the Rails framework. It will extract data straight from the repository and map it to useful statistics and graphs. Further it will outline some evolutionary analytics to see where the most changes within the project are occuring over time.

## Concept determination

<!-- What architectural information is needed to solve the problem? -->
<!-- Which viewpoints are relevant? -->

Before gathering the data from the codebase it is important to define the architectural information that is needed to solve the stated problem of gaining a better overview and understanding of Rails.
It is also benefical to set the viewpoints that are planned to use to show the gathered information.

From previous studies of Rails, like reading the documentation or looking at the root directory of the repository, it is clear that there are several components that form Rails. Good explanations what those individual comoponents do can be found in the documation. Something that would be useful to know is though:

- How complex are these components?
- How are the components connected to each other?
- How active is the development on them?

The concrete information that should be gathered is something like:

- Number of files in component
- Lines of code per file, per component
- Functions per file
- External dependencies per component
- Usuage between Rails components
- Commits with their modification to files/component

Useful viewpoints to make sense of the data would be:

- A simple table showing the lines of code per file and then per component
- A bar graph showing the total lines of code in a component
- A node, edge graph showing the dependency between components
- The same graphs can be used to show modifications on files over time

## Data gathering

In order to gather relevant information to answer the list of questions and ultimately solve the above stated problem, the Python language will be used.



## Knowledge inference

<!-- module view: nouns = nodes; verbs = dependencies/edges -->

## Information interpretation

## Conclusion
