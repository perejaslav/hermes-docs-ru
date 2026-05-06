On this page
Extract structured data from LLM responses with Pydantic validation, retry failed extractions automatically, parse complex JSON with type safety, and stream partial results with Instructor - battle-tested structured output library
## Skill metadata[​](<#skill-metadata> "Direct link to Skill metadata")
|   
---|---  
Source| Optional — install with `hermes skills install official/mlops/instructor`  
Path| `optional-skills/mlops/instructor`  
Version| `1.0.0`  
Author| Orchestra Research  
License| MIT  
Dependencies| `instructor`, `pydantic`, `openai`, `anthropic`  
Tags| `Prompt Engineering`, `Instructor`, `Structured Output`, `Pydantic`, `Data Extraction`, `JSON Parsing`, `Type Safety`, `Validation`, `Streaming`, `OpenAI`, `Anthropic`  
## Reference: full SKILL.md[​](<#reference-full-skillmd> "Direct link to Reference: full SKILL.md")
info
The following is the complete skill definition that Hermes loads when this skill is triggered. This is what the agent sees as instructions when the skill is active.
# Instructor: Structured LLM Outputs
## When to Use This Skill[​](<#when-to-use-this-skill> "Direct link to When to Use This Skill")
Use Instructor when you need to:
  * **Extract structured data** from LLM responses reliably
  * **Validate outputs** against Pydantic schemas automatically
  * **Retry failed extractions** with automatic error handling
  * **Parse complex JSON** with type safety and validation
  * **Stream partial results** for real-time processing
  * **Support multiple LLM providers** with consistent API


**GitHub Stars** : 15,000+ | **Battle-tested** : 100,000+ developers
## Installation[​](<#installation> "Direct link to Installation")
[code] 
    # Base installation  
    pip install instructor  
      
    # With specific providers  
    pip install "instructor[anthropic]"  # Anthropic Claude  
    pip install "instructor[openai]"     # OpenAI  
    pip install "instructor[all]"        # All providers  
    
[/code]
## Quick Start[​](<#quick-start> "Direct link to Quick Start")
### Basic Example: Extract User Data[​](<#basic-example-extract-user-data> "Direct link to Basic Example: Extract User Data")
[code] 
    import instructor  
    from pydantic import BaseModel  
    from anthropic import Anthropic  
      
    # Define output structure  
    class User(BaseModel):  
        name: str  
        age: int  
        email: str  
      
    # Create instructor client  
    client = instructor.from_anthropic(Anthropic())  
      
    # Extract structured data  
    user = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": "John Doe is 30 years old. His email is john@example.com"  
        }],  
        response_model=User  
    )  
      
    print(user.name)   # "John Doe"  
    print(user.age)    # 30  
    print(user.email)  # "john@example.com"  
    
[/code]
### With OpenAI[​](<#with-openai> "Direct link to With OpenAI")
[code] 
    from openai import OpenAI  
      
    client = instructor.from_openai(OpenAI())  
      
    user = client.chat.completions.create(  
        model="gpt-4o-mini",  
        response_model=User,  
        messages=[{"role": "user", "content": "Extract: Alice, 25, alice@email.com"}]  
    )  
    
[/code]
## Core Concepts[​](<#core-concepts> "Direct link to Core Concepts")
### 1\. Response Models (Pydantic)[​](<#1-response-models-pydantic> "Direct link to 1. Response Models \(Pydantic\)")
Response models define the structure and validation rules for LLM outputs.
#### Basic Model[​](<#basic-model> "Direct link to Basic Model")
[code] 
    from pydantic import BaseModel, Field  
      
    class Article(BaseModel):  
        title: str = Field(description="Article title")  
        author: str = Field(description="Author name")  
        word_count: int = Field(description="Number of words", gt=0)  
        tags: list[str] = Field(description="List of relevant tags")  
      
    article = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": "Analyze this article: [article text]"  
        }],  
        response_model=Article  
    )  
    
[/code]
**Benefits:**
  * Type safety with Python type hints
  * Automatic validation (word_count > 0)
  * Self-documenting with Field descriptions
  * IDE autocomplete support


#### Nested Models[​](<#nested-models> "Direct link to Nested Models")
[code] 
    class Address(BaseModel):  
        street: str  
        city: str  
        country: str  
      
    class Person(BaseModel):  
        name: str  
        age: int  
        address: Address  # Nested model  
      
    person = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": "John lives at 123 Main St, Boston, USA"  
        }],  
        response_model=Person  
    )  
      
    print(person.address.city)  # "Boston"  
    
[/code]
#### Optional Fields[​](<#optional-fields> "Direct link to Optional Fields")
[code] 
    from typing import Optional  
      
    class Product(BaseModel):  
        name: str  
        price: float  
        discount: Optional[float] = None  # Optional  
        description: str = Field(default="No description")  # Default value  
      
    # LLM doesn't need to provide discount or description  
    
[/code]
#### Enums for Constraints[​](<#enums-for-constraints> "Direct link to Enums for Constraints")
[code] 
    from enum import Enum  
      
    class Sentiment(str, Enum):  
        POSITIVE = "positive"  
        NEGATIVE = "negative"  
        NEUTRAL = "neutral"  
      
    class Review(BaseModel):  
        text: str  
        sentiment: Sentiment  # Only these 3 values allowed  
      
    review = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": "This product is amazing!"  
        }],  
        response_model=Review  
    )  
      
    print(review.sentiment)  # Sentiment.POSITIVE  
    
[/code]
### 2\. Validation[​](<#2-validation> "Direct link to 2. Validation")
Pydantic validates LLM outputs automatically. If validation fails, Instructor retries.
#### Built-in Validators[​](<#built-in-validators> "Direct link to Built-in Validators")
[code] 
    from pydantic import Field, EmailStr, HttpUrl  
      
    class Contact(BaseModel):  
        name: str = Field(min_length=2, max_length=100)  
        age: int = Field(ge=0, le=120)  # 0 <= age <= 120  
        email: EmailStr  # Validates email format  
        website: HttpUrl  # Validates URL format  
      
    # If LLM provides invalid data, Instructor retries automatically  
    
[/code]
#### Custom Validators[​](<#custom-validators> "Direct link to Custom Validators")
[code] 
    from pydantic import field_validator  
      
    class Event(BaseModel):  
        name: str  
        date: str  
        attendees: int  
      
        @field_validator('date')  
        def validate_date(cls, v):  
            """Ensure date is in YYYY-MM-DD format."""  
            import re  
            if not re.match(r'\d{4}-\d{2}-\d{2}', v):  
                raise ValueError('Date must be YYYY-MM-DD format')  
            return v  
      
        @field_validator('attendees')  
        def validate_attendees(cls, v):  
            """Ensure positive attendees."""  
            if v < 1:  
                raise ValueError('Must have at least 1 attendee')  
            return v  
    
[/code]
#### Model-Level Validation[​](<#model-level-validation> "Direct link to Model-Level Validation")
[code] 
    from pydantic import model_validator  
      
    class DateRange(BaseModel):  
        start_date: str  
        end_date: str  
      
        @model_validator(mode='after')  
        def check_dates(self):  
            """Ensure end_date is after start_date."""  
            from datetime import datetime  
            start = datetime.strptime(self.start_date, '%Y-%m-%d')  
            end = datetime.strptime(self.end_date, '%Y-%m-%d')  
      
            if end < start:  
                raise ValueError('end_date must be after start_date')  
            return self  
    
[/code]
### 3\. Automatic Retrying[​](<#3-automatic-retrying> "Direct link to 3. Automatic Retrying")
Instructor retries automatically when validation fails, providing error feedback to the LLM.
[code] 
    # Retries up to 3 times if validation fails  
    user = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": "Extract user from: John, age unknown"  
        }],  
        response_model=User,  
        max_retries=3  # Default is 3  
    )  
      
    # If age can't be extracted, Instructor tells the LLM:  
    # "Validation error: age - field required"  
    # LLM tries again with better extraction  
    
[/code]
**How it works:**
  1. LLM generates output
  2. Pydantic validates
  3. If invalid: Error message sent back to LLM
  4. LLM tries again with error feedback
  5. Repeats up to max_retries


### 4\. Streaming[​](<#4-streaming> "Direct link to 4. Streaming")
Stream partial results for real-time processing.
#### Streaming Partial Objects[​](<#streaming-partial-objects> "Direct link to Streaming Partial Objects")
[code] 
    from instructor import Partial  
      
    class Story(BaseModel):  
        title: str  
        content: str  
        tags: list[str]  
      
    # Stream partial updates as LLM generates  
    for partial_story in client.messages.create_partial(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": "Write a short sci-fi story"  
        }],  
        response_model=Story  
    ):  
        print(f"Title: {partial_story.title}")  
        print(f"Content so far: {partial_story.content[:100]}...")  
        # Update UI in real-time  
    
[/code]
#### Streaming Iterables[​](<#streaming-iterables> "Direct link to Streaming Iterables")
[code] 
    class Task(BaseModel):  
        title: str  
        priority: str  
      
    # Stream list items as they're generated  
    tasks = client.messages.create_iterable(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": "Generate 10 project tasks"  
        }],  
        response_model=Task  
    )  
      
    for task in tasks:  
        print(f"- {task.title} ({task.priority})")  
        # Process each task as it arrives  
    
[/code]
## Provider Configuration[​](<#provider-configuration> "Direct link to Provider Configuration")
### Anthropic Claude[​](<#anthropic-claude> "Direct link to Anthropic Claude")
[code] 
    import instructor  
    from anthropic import Anthropic  
      
    client = instructor.from_anthropic(  
        Anthropic(api_key="your-api-key")  
    )  
      
    # Use with Claude models  
    response = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[...],  
        response_model=YourModel  
    )  
    
[/code]
### OpenAI[​](<#openai> "Direct link to OpenAI")
[code] 
    from openai import OpenAI  
      
    client = instructor.from_openai(  
        OpenAI(api_key="your-api-key")  
    )  
      
    response = client.chat.completions.create(  
        model="gpt-4o-mini",  
        response_model=YourModel,  
        messages=[...]  
    )  
    
[/code]
### Local Models (Ollama)[​](<#local-models-ollama> "Direct link to Local Models \(Ollama\)")
[code] 
    from openai import OpenAI  
      
    # Point to local Ollama server  
    client = instructor.from_openai(  
        OpenAI(  
            base_url="http://localhost:11434/v1",  
            api_key="ollama"  # Required but ignored  
        ),  
        mode=instructor.Mode.JSON  
    )  
      
    response = client.chat.completions.create(  
        model="llama3.1",  
        response_model=YourModel,  
        messages=[...]  
    )  
    
[/code]
## Common Patterns[​](<#common-patterns> "Direct link to Common Patterns")
### Pattern 1: Data Extraction from Text[​](<#pattern-1-data-extraction-from-text> "Direct link to Pattern 1: Data Extraction from Text")
[code] 
    class CompanyInfo(BaseModel):  
        name: str  
        founded_year: int  
        industry: str  
        employees: int  
        headquarters: str  
      
    text = """  
    Tesla, Inc. was founded in 2003. It operates in the automotive and energy  
    industry with approximately 140,000 employees. The company is headquartered  
    in Austin, Texas.  
    """  
      
    company = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": f"Extract company information from: {text}"  
        }],  
        response_model=CompanyInfo  
    )  
    
[/code]
### Pattern 2: Classification[​](<#pattern-2-classification> "Direct link to Pattern 2: Classification")
[code] 
    class Category(str, Enum):  
        TECHNOLOGY = "technology"  
        FINANCE = "finance"  
        HEALTHCARE = "healthcare"  
        EDUCATION = "education"  
        OTHER = "other"  
      
    class ArticleClassification(BaseModel):  
        category: Category  
        confidence: float = Field(ge=0.0, le=1.0)  
        keywords: list[str]  
      
    classification = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": "Classify this article: [article text]"  
        }],  
        response_model=ArticleClassification  
    )  
    
[/code]
### Pattern 3: Multi-Entity Extraction[​](<#pattern-3-multi-entity-extraction> "Direct link to Pattern 3: Multi-Entity Extraction")
[code] 
    class Person(BaseModel):  
        name: str  
        role: str  
      
    class Organization(BaseModel):  
        name: str  
        industry: str  
      
    class Entities(BaseModel):  
        people: list[Person]  
        organizations: list[Organization]  
        locations: list[str]  
      
    text = "Tim Cook, CEO of Apple, announced at the event in Cupertino..."  
      
    entities = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": f"Extract all entities from: {text}"  
        }],  
        response_model=Entities  
    )  
      
    for person in entities.people:  
        print(f"{person.name} - {person.role}")  
    
[/code]
### Pattern 4: Structured Analysis[​](<#pattern-4-structured-analysis> "Direct link to Pattern 4: Structured Analysis")
[code] 
    class SentimentAnalysis(BaseModel):  
        overall_sentiment: Sentiment  
        positive_aspects: list[str]  
        negative_aspects: list[str]  
        suggestions: list[str]  
        score: float = Field(ge=-1.0, le=1.0)  
      
    review = "The product works well but setup was confusing..."  
      
    analysis = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[{  
            "role": "user",  
            "content": f"Analyze this review: {review}"  
        }],  
        response_model=SentimentAnalysis  
    )  
    
[/code]
### Pattern 5: Batch Processing[​](<#pattern-5-batch-processing> "Direct link to Pattern 5: Batch Processing")
[code] 
    def extract_person(text: str) -> Person:  
        return client.messages.create(  
            model="claude-sonnet-4-5-20250929",  
            max_tokens=1024,  
            messages=[{  
                "role": "user",  
                "content": f"Extract person from: {text}"  
            }],  
            response_model=Person  
        )  
      
    texts = [  
        "John Doe is a 30-year-old engineer",  
        "Jane Smith, 25, works in marketing",  
        "Bob Johnson, age 40, software developer"  
    ]  
      
    people = [extract_person(text) for text in texts]  
    
[/code]
## Advanced Features[​](<#advanced-features> "Direct link to Advanced Features")
### Union Types[​](<#union-types> "Direct link to Union Types")
[code] 
    from typing import Union  
      
    class TextContent(BaseModel):  
        type: str = "text"  
        content: str  
      
    class ImageContent(BaseModel):  
        type: str = "image"  
        url: HttpUrl  
        caption: str  
      
    class Post(BaseModel):  
        title: str  
        content: Union[TextContent, ImageContent]  # Either type  
      
    # LLM chooses appropriate type based on content  
    
[/code]
### Dynamic Models[​](<#dynamic-models> "Direct link to Dynamic Models")
[code] 
    from pydantic import create_model  
      
    # Create model at runtime  
    DynamicUser = create_model(  
        'User',  
        name=(str, ...),  
        age=(int, Field(ge=0)),  
        email=(EmailStr, ...)  
    )  
      
    user = client.messages.create(  
        model="claude-sonnet-4-5-20250929",  
        max_tokens=1024,  
        messages=[...],  
        response_model=DynamicUser  
    )  
    
[/code]
### Custom Modes[​](<#custom-modes> "Direct link to Custom Modes")
[code] 
    # For providers without native structured outputs  
    client = instructor.from_anthropic(  
        Anthropic(),  
        mode=instructor.Mode.JSON  # JSON mode  
    )  
      
    # Available modes:  
    # - Mode.ANTHROPIC_TOOLS (recommended for Claude)  
    # - Mode.JSON (fallback)  
    # - Mode.TOOLS (OpenAI tools)  
    
[/code]
### Context Management[​](<#context-management> "Direct link to Context Management")
[code] 
    # Single-use client  
    with instructor.from_anthropic(Anthropic()) as client:  
        result = client.messages.create(  
            model="claude-sonnet-4-5-20250929",  
            max_tokens=1024,  
            messages=[...],  
            response_model=YourModel  
        )  
        # Client closed automatically  
    
[/code]
## Error Handling[​](<#error-handling> "Direct link to Error Handling")
### Handling Validation Errors[​](<#handling-validation-errors> "Direct link to Handling Validation Errors")
[code] 
    from pydantic import ValidationError  
      
    try:  
        user = client.messages.create(  
            model="claude-sonnet-4-5-20250929",  
            max_tokens=1024,  
            messages=[...],  
            response_model=User,  
            max_retries=3  
        )  
    except ValidationError as e:  
        print(f"Failed after retries: {e}")  
        # Handle gracefully  
      
    except Exception as e:  
        print(f"API error: {e}")  
    
[/code]
### Custom Error Messages[​](<#custom-error-messages> "Direct link to Custom Error Messages")
[code] 
    class ValidatedUser(BaseModel):  
        name: str = Field(description="Full name, 2-100 characters")  
        age: int = Field(description="Age between 0 and 120", ge=0, le=120)  
        email: EmailStr = Field(description="Valid email address")  
      
        class Config:  
            # Custom error messages  
            json_schema_extra = {  
                "examples": [  
                    {  
                        "name": "John Doe",  
                        "age": 30,  
                        "email": "john@example.com"  
                    }  
                ]  
            }  
    
[/code]
## Best Practices[​](<#best-practices> "Direct link to Best Practices")
### 1\. Clear Field Descriptions[​](<#1-clear-field-descriptions> "Direct link to 1. Clear Field Descriptions")
[code] 
    # ❌ Bad: Vague  
    class Product(BaseModel):  
        name: str  
        price: float  
      
    # ✅ Good: Descriptive  
    class Product(BaseModel):  
        name: str = Field(description="Product name from the text")  
        price: float = Field(description="Price in USD, without currency symbol")  
    
[/code]
### 2\. Use Appropriate Validation[​](<#2-use-appropriate-validation> "Direct link to 2. Use Appropriate Validation")
[code] 
    # ✅ Good: Constrain values  
    class Rating(BaseModel):  
        score: int = Field(ge=1, le=5, description="Rating from 1 to 5 stars")  
        review: str = Field(min_length=10, description="Review text, at least 10 chars")  
    
[/code]
### 3\. Provide Examples in Prompts[​](<#3-provide-examples-in-prompts> "Direct link to 3. Provide Examples in Prompts")
[code] 
    messages = [{  
        "role": "user",  
        "content": """Extract person info from: "John, 30, engineer"  
      
    Example format:  
    {  
      "name": "John Doe",  
      "age": 30,  
      "occupation": "engineer"  
    }"""  
    }]  
    
[/code]
### 4\. Use Enums for Fixed Categories[​](<#4-use-enums-for-fixed-categories> "Direct link to 4. Use Enums for Fixed Categories")
[code] 
    # ✅ Good: Enum ensures valid values  
    class Status(str, Enum):  
        PENDING = "pending"  
        APPROVED = "approved"  
        REJECTED = "rejected"  
      
    class Application(BaseModel):  
        status: Status  # LLM must choose from enum  
    
[/code]
### 5\. Handle Missing Data Gracefully[​](<#5-handle-missing-data-gracefully> "Direct link to 5. Handle Missing Data Gracefully")
[code] 
    class PartialData(BaseModel):  
        required_field: str  
        optional_field: Optional[str] = None  
        default_field: str = "default_value"  
      
    # LLM only needs to provide required_field  
    
[/code]
## Comparison to Alternatives[​](<#comparison-to-alternatives> "Direct link to Comparison to Alternatives")
Feature| Instructor| Manual JSON| LangChain| DSPy  
---|---|---|---|---  
Type Safety| ✅ Yes| ❌ No| ⚠️ Partial| ✅ Yes  
Auto Validation| ✅ Yes| ❌ No| ❌ No| ⚠️ Limited  
Auto Retry| ✅ Yes| ❌ No| ❌ No| ✅ Yes  
Streaming| ✅ Yes| ❌ No| ✅ Yes| ❌ No  
Multi-Provider| ✅ Yes| ⚠️ Manual| ✅ Yes| ✅ Yes  
Learning Curve| Low| Low| Medium| High  
**When to choose Instructor:**
  * Need structured, validated outputs
  * Want type safety and IDE support
  * Require automatic retries
  * Building data extraction systems


**When to choose alternatives:**
  * DSPy: Need prompt optimization
  * LangChain: Building complex chains
  * Manual: Simple, one-off extractions


## Resources[​](<#resources> "Direct link to Resources")
  * **Documentation** : <https://python.useinstructor.com>
  * **GitHub** : <https://github.com/jxnl/instructor> (15k+ stars)
  * **Cookbook** : <https://python.useinstructor.com/examples>
  * **Discord** : Community support available


## See Also[​](<#see-also> "Direct link to See Also")
  * `references/validation.md` \- Advanced validation patterns
  * `references/providers.md` \- Provider-specific configuration
  * `references/examples.md` \- Real-world use cases


  * [Skill metadata](<#skill-metadata>)
  * [Reference: full SKILL.md](<#reference-full-skillmd>)
  * [When to Use This Skill](<#when-to-use-this-skill>)
  * [Installation](<#installation>)
  * [Quick Start](<#quick-start>)
    * [Basic Example: Extract User Data](<#basic-example-extract-user-data>)
    * [With OpenAI](<#with-openai>)
  * [Core Concepts](<#core-concepts>)
    * [1\. Response Models (Pydantic)](<#1-response-models-pydantic>)
    * [2\. Validation](<#2-validation>)
    * [3\. Automatic Retrying](<#3-automatic-retrying>)
    * [4\. Streaming](<#4-streaming>)
  * [Provider Configuration](<#provider-configuration>)
    * [Anthropic Claude](<#anthropic-claude>)
    * [OpenAI](<#openai>)
    * [Local Models (Ollama)](<#local-models-ollama>)
  * [Common Patterns](<#common-patterns>)
    * [Pattern 1: Data Extraction from Text](<#pattern-1-data-extraction-from-text>)
    * [Pattern 2: Classification](<#pattern-2-classification>)
    * [Pattern 3: Multi-Entity Extraction](<#pattern-3-multi-entity-extraction>)
    * [Pattern 4: Structured Analysis](<#pattern-4-structured-analysis>)
    * [Pattern 5: Batch Processing](<#pattern-5-batch-processing>)
  * [Advanced Features](<#advanced-features>)
    * [Union Types](<#union-types>)
    * [Dynamic Models](<#dynamic-models>)
    * [Custom Modes](<#custom-modes>)
    * [Context Management](<#context-management>)
  * [Error Handling](<#error-handling>)
    * [Handling Validation Errors](<#handling-validation-errors>)
    * [Custom Error Messages](<#custom-error-messages>)
  * [Best Practices](<#best-practices>)
    * [1\. Clear Field Descriptions](<#1-clear-field-descriptions>)
    * [2\. Use Appropriate Validation](<#2-use-appropriate-validation>)
    * [3\. Provide Examples in Prompts](<#3-provide-examples-in-prompts>)
    * [4\. Use Enums for Fixed Categories](<#4-use-enums-for-fixed-categories>)
    * [5\. Handle Missing Data Gracefully](<#5-handle-missing-data-gracefully>)
  * [Comparison to Alternatives](<#comparison-to-alternatives>)
  * [Resources](<#resources>)
  * [See Also](<#see-also>)




<!-- Source: https://hermes-agent.nousresearch.com/docs/user-guide/skills/optional/mlops/mlops-instructor -->
