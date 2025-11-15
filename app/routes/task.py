from fastapi import APIRouter, Depends, status, HTTPException
from fastapi import Request
from typing import List, Optional
from app.models.task import Task
from app.schemas.user import *
from app.utils.helper_functions import *
from app.utils.oauth import *
from app.utils.enum import *
from app.database import *
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession, types


router = APIRouter()
@router.post("/search/", status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate,  
                      current_user: int = Depends(get_current_user),
):
    try:
        with DBFactory() as db:
            query =task.prompt_or_query
            url=settings.MCP_SEARCH_URL
            # url=url+f"query={query}"
            async with streamablehttp_client(url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # List available tools
                    tools_result = await session.list_tools()
                    # print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")
                    result = await session.call_tool(
                    name="search",
                    arguments={"query": query}
                )
    
                    # for item in result.content:
                    #     print(item.text)

            content_str = ""
            if result.content:
                content_str = "\n".join([item.text for item in result.content if isinstance(item, types.TextContent)])

            new_user = Task(type="search",user_id=current_user.id,prompt_or_query=task.prompt_or_query,content=content_str)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {"message": "Task Created Successfully","content":result.content}

    except HTTPException as error:
        raise error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error
    

@router.post("/image/", status_code=status.HTTP_201_CREATED)
async def generate_imaget(task: TaskCreate,  
                      current_user: int = Depends(get_current_user),
):
    try:
        with DBFactory() as db:
            query =task.prompt_or_query
            url=settings.MCP_IMAGE_URL
            # url=url+f"prompt={query}"
            # db.add(new_task)
            # db.commit()
            # db.refresh(new_task)
            async with streamablehttp_client(url) as (read, write, _):
                async with ClientSession(read, write) as session:
                    # Initialize the connection
                    await session.initialize()
                    
                    # List available tools
                    tools_result = await session.list_tools()
                    # print(f"Available tools: {', '.join([t.name for t in tools_result.tools])}")
                    result = await session.call_tool(
                    name="generateImageUrl",
                    arguments={"prompt": query}
                )
    
                    # for item in result.content:
                    #     print(item.text)

            print(result.content)
            content_str = ""
            if result.content and hasattr(result.content[0], 'text'):
                 # Assuming the first content item has the image URL in 'text'
                content_str = result.content[0].text

            new_user = Task(type="image",user_id=current_user.id,prompt_or_query=task.prompt_or_query,content=content_str)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            return {"message": "Task Created Successfully","content":result.content[0]}

    except HTTPException as error:
        raise error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error
    

@router.get("/tasks/", status_code=status.HTTP_200_OK)
async def get_tasks(
    type: Optional[ContentType] = None,
    current_user: int = Depends(get_current_user),
):
    try:
        with DBFactory() as db:
            tasks = Task.get_tasks_by_user(db, user_id=current_user.id, task_type=type)
            if type is None:
                for each in tasks:
                    del each.user_id
            else:
                for each in tasks:
                    del each.user_id   
                    del each.type
            return tasks

    except HTTPException as error:
        raise error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    task_id: str,
    current_user: int = Depends(get_current_user),
):
    try:
        with DBFactory() as db:
            task = Task.get_task_by_id(db, task_id=task_id)

            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
                )

            if task.user_id != current_user.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action"
                )

            db.delete(task)
            db.commit()

            return {"message": "Task deleted successfully"}

    except HTTPException as error:
        raise error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error


@router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def update_task(
    task_id: str,
    task: TaskUpdate,
    current_user: int = Depends(get_current_user),
):
    try:
        with DBFactory() as db:
            db_task = Task.get_task_by_id(db, task_id=task_id)

            if not db_task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
                )

            if db_task.user_id != current_user.id:
                raise HTTPException(
                    status.HTTP_401_UNAUTHORIZED, detail="Not authorized to perform requested action"
                )

            if task.prompt_or_query:
                db_task.prompt_or_query = task.prompt_or_query
            if task.content:
                db_task.content = task.content
            if task.notes:
                db_task.notes = task.notes

            db.commit()
            db.refresh(db_task)

            del db_task.user_id
            del db_task.type

            return db_task

    except HTTPException as error:
        raise error

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(error)
        ) from error