from .filesystem import FilesystemChunkStore


class ChunkStoreFactory:

    @staticmethod
    def create(root_dir, config):

        if config["type"] == "filesystem":
            return FilesystemChunkStore(
                root_dir, 
                output_directory=config["output_directory"]
            )

        raise ValueError(
            f"Unsupported chunk store: {config['type']}"
        )