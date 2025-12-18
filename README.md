# MCP Server Example
This is a starter example to understand the MCP protocol, which has two tools.
1. Image : Downloads an image for a user specified city
2. World Fact : Retrieve a random world fact in a language you understand

## Image Tool

1. User enters a city, if it is not available, we ask user for an alternative.  
![Image - Screen 1.png](Images/Image%20-%20Screen%201.png)  
2. If user agrees to the alternative, we show them the requested image.  
![Image - Screen 2.png](Images/Image%20-%20Screen%202.png)  

## World Fact Tool
1. User is prompted for the language options  
![Text - Screen 1.png](Images/Text%20-%20Screen%201.png)  
2. User can select from the drop-down of available languages  
![Text - Screen 2.png](Images/Text%20-%20Screen%202.png)  
3. Fact is retrieved in the language selected  
![Text - Screen 3.png](Images/Text%20-%20Screen%203.png)  

## Installation
```
uv sync
```