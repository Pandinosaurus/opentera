from services.FileTransferService.libfiletransferservice.db.Base import db
from opentera.db.Base import BaseModel
from sqlalchemy import exc
import os


class AssetFileData(db.Model, BaseModel):
    __tablename__ = "t_asset_file_data"
    id_asset_file_data = db.Column(db.Integer, db.Sequence('id_asset_file_data_sequence'),
                                   primary_key=True, autoincrement=True)

    asset_uuid = db.Column(db.String(36), nullable=False, unique=True)
    asset_original_filename = db.Column(db.String, nullable=False)
    asset_file_size = db.Column(db.BigInteger, nullable=False)
    # asset_md5 = db.Column(db.String, nullable=False)  # Not used now

    @staticmethod
    def get_asset_for_uuid(uuid_asset: str):
        return AssetFileData.query.filter_by(asset_uuid=uuid_asset).first()

    @staticmethod
    def get_assets_for_uuids(uuids_asset: list):
        return AssetFileData.query.filter(AssetFileData.asset_uuid.in_(uuids_asset)).all()

    # Delete this asset. file_folder is required to delete the file too.
    def delete_file_asset(self, file_folder: str) -> bool:
        # Delete related file from system
        file_name = os.path.join(file_folder, self.asset_uuid)
        if os.path.exists(file_name):
            # print('AssetFileData: Deleted ' + file_name)
            os.remove(file_name)
        else:
            # print('AssetFileData: File not found: ' + file_name)
            return False

        # Delete self from database
        try:
            db.session.delete(self)
            self.commit()
        except exc.SQLAlchemyError:
            return False

        return True

    # def delete(self, id_todel):
    #     AssetFileData.delete_files([self])
    #
    #     # Delete data from the database
    #     db.session.delete(self)
    #     db.session.commit()
    #
    # @staticmethod
    # def delete_files(assets: list):
    #     # Get upload path from configuration
    #     from services.FileTransferService.Globals import config_man
    #     file_path = config_man.filetransfer_config['upload_directory']
    #
    #     for data in assets:
    #         file_name = os.path.join(file_path, data.devicedata_uuid)
    #         if os.path.exists(file_name):
    #             print('AssetFileData: Deleted ' + file_name)
    #             os.remove(file_name)
    #         else:
    #             print('AssetFileData: File not found: ' + file_name)
