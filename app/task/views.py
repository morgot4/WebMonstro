from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

router = APIRouter(prefix="/task")

TASKS_FOLDER = "C:\\Users\\Administrator\\Desktop\\"


@router.get("/file/{filename}")
async def get_task_file(filename):
    try:
        return FileResponse(
            path=TASKS_FOLDER + "\\" + filename + ".txt", status_code=status.HTTP_200_OK
        )
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="file with this name not found",
        )
