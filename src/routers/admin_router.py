# routers/admin_router.py (only backup/restore part shown)

from fastapi import APIRouter, Request, HTTPException, UploadFile, File
from db.dependencies import GetDBAdmin, GetUID
from core.limiter import limiter
from services.admin_services import AdminServices
from services.admin.backup_and_restore import Backup
from models.admin_models import AdminModel
from utils.logs import create_log  # type: ignore
from fastapi.responses import StreamingResponse

router = APIRouter(prefix="/admin")

# ... your existing create/read/update/delete user routes ...

# ---------- CREATE BACKUP ----------
@router.post("/create_backup")
@limiter.limit("5/second")  # type: ignore
def create_backup(
    request: Request,
    db: GetDBAdmin,
    uid: GetUID,
    folder: str | None = None,  # can pass ?folder=prod if you want
):
    try:
        file_name = Backup.create(db, folder)

        create_log(
            type="LOG",
            description="admin: created backup",
            user_id=uid,
            endpoint="/admin/create_backup",
            data={"file_name": file_name, "folder": folder},
        )

        return {"message": "Backup created", "file_name": file_name}
    except Exception as e:
        create_log(
            type="ERROR",
            description="admin: failed to create backup",
            user_id=uid,
            endpoint="/admin/create_backup",
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=f"Error creating backup: {str(e)}")


# ---------- LIST BACKUPS ----------
@router.get("/backups")
@limiter.limit("5/second")  # type: ignore
def list_backups(
    request: Request,
    db: GetDBAdmin,
    uid: GetUID,
    folder: str | None = None,
):
    try:
        backups = Backup.list_backups(db, folder)

        create_log(
            type="LOG",
            description="admin: listed backups",
            user_id=uid,
            endpoint="/admin/backups",
            data={"count": len(backups), "folder": folder},
        )

        return backups
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing backups: {str(e)}")


# ---------- DOWNLOAD BACKUP (for browser download) ----------
@router.get("/backups/download")
@limiter.limit("5/second")  # type: ignore
def download_backup(
    request: Request,
    db: GetDBAdmin,
    uid: GetUID,
    file_name: str,
):
    try:
        file_bytes = Backup.get_backup_bytes(db, file_name)

        create_log(
            type="LOG",
            description="admin: downloaded backup",
            user_id=uid,
            endpoint="/admin/backups/download",
            data={"file_name": file_name},
        )

        return StreamingResponse(
            iter([file_bytes]),
            media_type="application/json",
            headers={
                "Content-Disposition": f'attachment; filename="{Path(file_name).name}"'
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading backup: {str(e)}")


# ---------- RESTORE FROM STORED BACKUP ----------
@router.post("/restore_from_backup")
@limiter.limit("5/second")  # type: ignore
def restore_from_backup(
    request: Request,
    db: GetDBAdmin,
    uid: GetUID,
    file_name: str | None = None,  # ?file_name=... or omit to use latest
    folder: str | None = None,
):
    try:
        used_file = Backup.restore(db, file_name=file_name, folder=folder)

        create_log(
            type="LOG",
            description="admin: restored from backup",
            user_id=uid,
            endpoint="/admin/restore_from_backup",
            data={"file_name": used_file, "folder": folder},
        )

        return {"message": "Restore completed", "file_name": used_file}
    except Exception as e:
        create_log(
            type="ERROR",
            description="admin: failed to restore from backup",
            user_id=uid,
            endpoint="/admin/restore_from_backup",
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=f"Error restoring from backup: {str(e)}")


# ---------- RESTORE FROM UPLOADED FILE ----------
@router.post("/restore_from_upload")
@limiter.limit("5/second")  # type: ignore
async def restore_from_upload(
    request: Request,
    db: GetDBAdmin,
    uid: GetUID,
    file: UploadFile = File(...),
):
    try:
        file_bytes = await file.read()
        used_file = Backup.restore_from_bytes(db, file_bytes)

        create_log(
            type="LOG",
            description="admin: restored from uploaded backup file",
            user_id=uid,
            endpoint="/admin/restore_from_upload",
            data={"file_name": used_file, "uploaded_name": file.filename},
        )

        return {"message": "Restore from uploaded file completed", "file_name": used_file}
    except Exception as e:
        create_log(
            type="ERROR",
            description="admin: failed to restore from uploaded backup",
            user_id=uid,
            endpoint="/admin/restore_from_upload",
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=f"Error restoring from uploaded backup: {str(e)}")
