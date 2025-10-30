from typing import TypeVar, cast, TYPE_CHECKING
from ._auth import get_sheet
from ._manager import GModelManager
from .exceptions import FieldException
from .field import Field

if TYPE_CHECKING:
    from typing import Type, Any


class GModelMeta(type):

	def __new__(mcs, name: str, bases: tuple, attrs: dict, **kwargs):
		cls = super().__new__(mcs, name, bases, attrs, **kwargs)
		if name != "GModel":
			# Process fields immediately during class creation
			cls._meta = {}
			cls._errors = {}
			cls_annotations = {}
			for attr, obj in list(attrs.items()):
				if isinstance(obj, Field):
					delattr(cls, attr)
					cls._meta[attr] = obj
					cls_annotations[attr] = str
			
			setattr(cls, "__annotations__", cls_annotations)
			
			def _setup_attrs():
				class_meta = getattr(cls, "Meta")

				spreed_sheet = get_sheet(getattr(class_meta, "sheet_name", "default"))
				cls._data = spreed_sheet.worksheet(getattr(class_meta, "tab_name"))
				cls._headers = cls._data.row_values(getattr(class_meta, "header_index"))

				# Validate fields now that we have headers
				for attr, field_obj in cls._meta.items():
					try:
						field_obj.validate(cls._headers)
					except FieldException as ex:
						cls._errors[attr] = str(ex)
					except Exception as ex:
						print(ex)

			# Create properly typed manager instance for this specific model class
			manager_instance = GModelManager(cls, _setup_attrs)
			setattr(cls, "manager", manager_instance)

		return cls
