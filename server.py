import base64
import httpx
from languages import language_codes
from dotenv import dotenv_values
from fastmcp import (
    FastMCP,
    Context
)
from mcp.types import ImageContent
from pathlib import Path

parent_path:Path = Path(__file__).resolve().parent
configs:dict = dotenv_values(parent_path / ".env")
secrets:dict = dotenv_values(parent_path / ".env.secret")
languages:list = [l.title() for l in language_codes.keys()]

mcp = FastMCP("Image and World Fact Server")

async def get_image(url:str) -> ImageContent | str:
    """
        Get an image from the specified URL.
        :parameter url: URL for the image to be downloaded
        :return: image: ImageContent object of the image
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            encoded_bytes = base64.b64encode(response.content)
            encoded_str = encoded_bytes.decode('utf-8')
            return ImageContent(
                data=encoded_str,
                type="image",
                mimeType="image/jpeg"
            )
        except httpx.HTTPStatusError as err:
            return err.response.text

@mcp.tool()
async def get_random_world_fact(ctx:Context) -> str:
    """
        Get a random world fact in the language specified by the language parameter.
        :parameter ctx: Context which is used to source more information from the user
        :return: str: random world fact
    """
    result = await ctx.elicit(
        message=f"Please select the language in which you want the world fact?",
        response_type=languages
    )
    await ctx.info(f"Retrieving fact in {result.data}")

    if result.action != "accept":
        return f"No valid selection made"
    else:
        lang_code = language_codes.get(result.data.lower())
        headers = {
            "x-rapidapi-host": configs['RAPID_API_HOST'],
            "x-rapidapi-key": secrets['RAPID_API_KEY']
        }
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    configs['WORLD_FACT_API_HOST'],
                    params={"lang": lang_code},
                    headers=headers,
                    timeout=30
                )
                response.raise_for_status()
                return response.json()["text"]
            except httpx.HTTPStatusError as err:
                return err.response.text

@mcp.tool()
async def get_city_image(city:str, ctx: Context) -> ImageContent | str:
    """
        Downloads an image of the city specified by the user.
        :parameter city: The name of the city to download the image
        :parameter ctx: Context which is used to source more information from the user
    """
    if city.lower() != "boston":
        result = await ctx.elicit(
            message=f"No image available for {city}, would you like to get an image for the city of Boston?",
            response_type=None
        )
        if result.action == "accept":
            return await get_image(configs['IMAGE_URL'])
        elif result.action == "decline":
            return "User does not want the image for Boston"
        else:
            return "Action cancelled by user"
    else:
        return await get_image(configs['IMAGE_URL'])

if __name__ == "__main__":
    mcp.run()
