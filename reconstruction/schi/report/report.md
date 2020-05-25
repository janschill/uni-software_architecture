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

<!-- TODO: explain the views, All these -->

## Data gathering

In order to gather relevant information to answer the list of questions and ultimately solve the above stated problem, the Python language will be used with a few useful libraries to make the extraction of data easier.
For the problem to solve two different sources of data will be used. Firstly the actual source code of Rails will be used and analysed, secondly the Git history will be looked at.
The source code for Rails is hosted on GitHub and can be easily cloned. With a clone the source code will be made available locally and additionally a hidden folder `.git` is created and populated, which holds all Git relavant data---also the history, that will used. Therefore, a clone of the repository make all data needed available.

```bash
$ git clone git@github.com:rails/rails.git
```

### Reconstruction

As before mentioned all components are in the root directory of the repository. The first step to see what components are available and load them into memory:

```python
directories = []
for (dirpath, dirnames, filenames) in walk('/path/to/rails'):
    directories.extend(dirnames)
    break
directories = list(filter(lambda x: x[0] != ".", directories)) # filter away all hidden directories
```

A look inside one of those directories will give an overview of what a component actually is.
There has been a standard format established for the development of small libraries in the Ruby programming language. These libraries are called __gems__ and most often contain the following files:

- `lib/`: contains the source code
- `test/` or `spec/`: for the test files
- `Rakefile`: uses Rake to automate tasks, like testing, generating code
- `bin/`: includes executables and is loaded into the user's `PATH`
- `README.md`: for a descriptive text about the gem
- `*.gemspec`: holding general information, like author, version, external dependencies etc.

[What is a gem? – Guides RubyGems](https://guides.rubygems.org/what-is-a-gem/)

The directories give a good way to group and seperate the information gathered by gem, as the information extraction can just be done on the directories after each other and stored in a suitable data structure and as they are all in the same format adds to the convenience.

Rails components:

- `actioncable`
- `actionmailbox`
- `actionmailer`
- `actionpack`
- `actiontext`
- `actionview`
- `activejob`
- `activemodel`
- `activerecord`
- `activestorage`
- `activesupport`
- `railties`

The project does not only include the Rails components but also other directories:

- `ci`
- `guides`
- `tasks`
- `tools`

These will be iterated and every file will be looked at.

```python
def get_files(path, file_extension):
    files = Path(path).rglob("*." + file_extension)
    meta_data_files = {}
    for file in files:
        meta_data_files[str(file)] = {
            'filename': str(file),
            'no_lines': number_of_lines(file),
            'no_functions': number_of_functions(file),
            'no_modules': number_of_modules(file),
            'no_requires': len(extract_require(file)),
            'functions': extract_functions(file),
            'requires': extract_require(file),
            'namespaces': extract_namespace(file),
            'autoloads': extract_autoload(file)
        }
    return meta_data_files
```

This loop will be called on the project root and given the Ruby file extension `rb`, to only look at Ruby files. This will count the number of lines, functions, modules, requires.
Modules can be counted by extracting on the key word `module`, it is used in Ruby to indicate a files namespace, which will then be used to import it into a different file. It is useful for grouping code that belongs together.

```ruby
module Mathematics
  module NumberTheory
    module Arithmetic
      def self.add(a, b)
        return a + b
      end
    end
  end
  module Geometry
  end
end

# Mathematics.NumberTheory.Arithmetic.add(1, 2) => 3
```

Using the `require` function is a way of importing files into the file that it is being called from. This is a good way of checking how many dependencies a file has to other files---showing possible complexity. There is one problem though: Rails, does not use this way of importing its own dependencies. What Rails does is, it uses an `autoload` function, that finds it in the path and loads it into the context of the library by having the class/file name passed to it.

```ruby
module ActionView
  # …
  autoload :Base # loads the file base.rb
  # …
end
```

This can be extracted and used to show what kind of files are being loaded on startup of the library and needed __globally__ for the library.

Further, the functions will be extracted. This list will hold a tuple of the function name and the line count.

A key function in the retrieval is this `extract_from_line` function. It will get a key word that it supposed to find on the provided line.
Regular expressions are used to find the key word and the wanted data, like the function name.

```python
def extract_from_line(name, line):
    if re.search("^([\s]*#)", line): # ignore comments
        return None
    elif name == 'def|end':
        method = re.search("^([\s]*(def |end)[ (\S+)]*)", line)
        return str(method.group(1)) if method else None
    elif name == 'module|class|end':
        namespace = re.search("^([\s]*(module|class|end)[ (\S+)]*)", line)
        return str(namespace.group(1)) if namespace else None
    else:
        x = re.search("" + name + " (\S+)", line)
        return None if x == None else str(x.group(1))
```

Because Ruby's syntax does not use any symbols indicating a block, but uses the off-side rule, just like Python, it is a bit trickier to extract functions and therefore, the code to do that is provided in the following listing.

```python
def extract_functions(file):
    functions = []
    line_count = 1
    current_function_name = ''
    def_identation = -1
    for ext in extract(file, 'def|end', True):
        # If ext is None, it means it did not find a nested def or
        # an ending to the function, thus incrementing
        if ext == None:
            line_count += 1
        else:
            identation = len(ext) - len(ext.lstrip(' '))
            # Single line function
            if 'def ' in ext and ' end' in ext:
                current_function_name = retrieve_function_name(ext)
                functions.append(add_function(current_function_name, 1))
            # Beginning of new function
            elif 'def ' in ext:
                def_identation = identation
                line_count = 0
                current_function_name = retrieve_function_name(ext)
            # Function ending
            elif 'end' in ext and identation == def_identation:
                functions.append(add_function(current_function_name, line_count))
                current_function_name = ''
                line_count = 1
            else:
                line_count += 1
    return functions
```

This function extracts every line from a file and checks what key word is present, based on that it will either start a new function, end one or just increment its line count.

The initial `get_files` function is being called when instantiating the `rails_components` object.

```python
rails_components = {}
for directory in directories:
    files = get_files(full_path('/' + directory + '/'), 'rb')
    average_LOC = int(reduce_by_key(files.values(), 'no_lines') / len(files.values()))
    average_NOF = int(reduce_by_key(files.values(), 'no_functions') / len(files.values()))
    average_requires = int(reduce_by_key(files.values(), 'no_requires') / len(files.values()))
    dependencies = get_external_dependencies(directory)
    rails_components[directory] = {
        'files': files,
        'average_LOC': average_LOC,
        'average_NOF': average_NOF,
        'average_requires': average_requires,
        'dependencies': dependencies }
rails_components = {k: v for k, v in sorted(rails_components.items(), key = lambda item: item[0])}
```

This will also add some general information, based on the gathered information about each individual component. Especially `dependencies` is of interested. The `.gemspec` file holds all the external gems that the current library depends on. This can be used to see how large the external complexity for the specific library is.

### Evolutionary

`PyDriller` exposes a class called `RepositoryMining`, that comes in handy when analysing a repository project.

```python
@functools.lru_cache(maxsize=None) # Memoize result for inputs
def count_file_modifications_simple(path, tag):
    commit_counts = defaultdict(int)
    for commit in RepositoryMining(path, from_tag=tag).traverse_commits():
        for modification in commit.modifications:
            try:
                commit_counts[modification.new_path] += 1
            except:
                pass
    return commit_counts
```

This function `count_file_modifications_simple` will count occurences of a file in the commit history, giving a good overview of the number of times a file has been changed over its history.
This implementation has the problem that it does not differentiate between, pure changes, deletion or additions of files. In order to handle these cases the modification object gives access to: `old_path` and `new_path`.

```python
# cc = {
#   'filename': occurrences in commit history,
#   'actionmailer/lib/action_mailer.rb': 113
# }
def handle_change_type(cc, commit, modification):
    new_path = modification.new_path
    old_path = modification.old_path
    try:
        # Change old_path to new_path, keep values
        if modification.change_type == ModificationType.RENAME:
            cc_old = cc.get(old_path, (0, []))
            cc[new_path] =  (cc_old[0] + 1, cc_old[1])
            cc.pop(old_path)
        elif modification.change_type == ModificationType.DELETE:
            cc.pop(old_path, '')
        elif modification.change_type == ModificationType.ADD:
            cc[new_path] = (1, [])
        else: # Modification to existing file
            count, cx = cc[old_path]
            comp = modification.complexity
            cc[old_path] = (count + 1, cx + [comp] if comp else cx)
    except Exception as e:
        pass
```

Another interesting metric is the complexity of a modifitaion. This is also recorded on most of the modifications and is realized as the [cyclomatic complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity).

Logical coupling can be used to detect modules that may depend on each other based on their frequency of change in the same commit. One can assume when two Rails components occur in the commit history often together that they depend on each other. This is of course no true indication like an actual dependency graph would give, but still valuable as it could give indications on dependencies that are not shown on dependency graphs generated from static analysis.

To couple the individual Rails components, firstly the components have to defined. This can be done manually as they do not change frequently and can be easily adapted when something gets added or removed.

```python
def rails_components():
    return [
        'activerecord', 'activesupport',
        'actionpack', 'railties',
        'actionview', 'activemodel',
        'activestorage', 'activejob',
        'actionmailbox', 'actioncable',
        'actiontext', 'actionmailer'
    ]
```

The original function that counts the change occurences of files can be reused, because it already loops over every commit and modification, so no reason to do it again.

```python
rails_components_dictionary = rails_components_dict()

# Returns the Rails component from the path
# actionmailer/lib/action_mailer.rb -> actionmailer
def changed_component(modification):
  return modification.old_path.rsplit('/')[0] or modification.new_path.rsplit('/')[0]

# cc = {
#   'filename': (occurrences in commit history, complexities),
#   'actionmailer/lib/action_mailer.rb': (113, [1,1,1,…]
# }
def logical_coupling(path):
    cc = defaultdict(lambda: (0, []))
    for commit in RepositoryMining(path).traverse_commits():
        # Holds all components that were touched in commit
        changed_components = []
        for modification in commit.modifications:
            # Holds changed component
            comp = changed_component(modification)
            # Check if it is a Rails component change
            if comp in rails_components():
                changed_components.append(comp)
            # Was the try-block in the previous version
            handle_change_type(cc, commit, modification)
        # Adds all changed components, but itself to the dictionary
        add_other_components(rails_components_dictionary, changed_components)
        # Reset the changed components for each commit
        changed_components = []

    return cc
```

All the information gathered in both processes will be plotted either by using basic `print` in a tabulated format or plotted by using `networkx` and `matplotlib`.

## Knowledge inference




| Component       | Ruby files | Ø LOC   | Ø Functions | Ø Requires | Dependencies |
|-----------------|------------|---------|-------------|------------|--------------|
| activerecord    | 853        | 160     | 12          | 1          | 2            |
| activesupport   | 469        | 119     | 10          | 1          | 5            |
| actionpack      | 325        | 202     | 16          | 1          | 6            |
| railties        | 278        | 148     | 9           | 3          | 5            |
| actionview      | 186        | 231     | 18          | 1          | 5            |
| activemodel     | 130        | 118     | 8           | 1          | 1            |
| activestorage   | 124        | 62      | 3           | 1          | 5            |
| activejob       | 118        | 70      | 4           | 1          | 2            |
| actionmailbox   | 93         | 34      | 1           | 0          | 6            |
| actioncable     | 86         | 79      | 6           | 1          | 4            |
| actiontext      | 74         | 35      | 2           | 0          | 5            |
| actionmailer    | 41         | 140     | 9           | 1          | 6            |
| guides          | 22         | 69      | 3           | 3          | 0            |
| tools           | 2          | 21      | 1           | 4          | 0            |
| ci              | 1          | 22      | 0           | 2          | 0            |
| tasks           | 1          | 323     | 5           | 6          | 0            |

__Figure 1 All Rails directories broken down by file__

| Component       | LOC    | NOF   |
|-----------------|--------|-------|
| activerecord    | 136860 | 10949 |
| actionpack      | 65919  | 5289  |
| activesupport   | 56011  | 4714  |
| actionview      | 43045  | 3474  |
| railties        | 41328  | 2653  |
| activemodel     | 15441  | 1071  |
| activejob       | 8265   | 559   |
| activestorage   | 7710   | 389   |
| actioncable     | 6846   | 535   |
| actionmailer    | 5742   | 369   |
| actionmailbox   | 3170   | 144   |
| actiontext      | 2625   | 174   |
| guides          | 1534   | 87    |
| tasks           | 323    | 5     |
| tools           | 43     | 2     |
| ci              | 22     | 0     |

__Figure 2 All Rails directories broken down by their total LOC and NOF__

<!-- module view: nouns = nodes; verbs = dependencies/edges -->

## Information interpretation

## Conclusion
