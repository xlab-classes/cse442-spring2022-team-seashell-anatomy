The form I created is super flexible and it'll be easy to add categories. 
Here's the input to create cetegories:

```
categories = [
  {'name': 'catA', 'type': 'checkbox', 'options': ['option1', 'option2']},
  {'name': 'catB', 'type': 'radio', 'options': ['option1', 'option2']},
  {'name': 'catC', 'type': 'range', 'options': ['option1', 'option2']},
  {'name': 'catD', 'type': 'text', 'options': ['option1', 'option2']},
]
```

The form would send a GET request to `/generate` with the form parameters as a query string. 
For example, the query string could look as follows: 

```
http://10.84.121.39:5001/generate?catA=option2&catB=option2&catC=67&catC=32&catD=option1&catD=option2
```

Each category can have as many options as we want, and be of any type we want. The code would render as follows:

<img width="400" alt="Screen Shot 2022-02-28 at 10 33 01 PM" src="https://user-images.githubusercontent.com/56481968/156444806-e8efd2d4-2823-4c02-a6cf-862bf02595ac.png">



The next steps are to create a new route in app.py for `/generate` that accepts the proper string, and parses/handles the data.
