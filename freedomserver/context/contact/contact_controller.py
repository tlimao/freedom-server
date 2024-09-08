import json

from aiohttp.web import Request, Response, json_response

from freedomlib.contact.contact import Contact
from freedomserver.context.contact.contact_service import ContactService

class ContactController:

    def __init__(self, contact_service: ContactService) -> None:
        self._contact_service: ContactService = contact_service

    async def contacts_info(self, request: Request) -> Response:
        try:
            phonenumbers: list[str] = await request.json()
            contacts: list[Contact] = self._contact_service.get_contacts(phonenumbers)
            
            return json_response(status=200, data=[contact.to_dict() for contact in contacts])
        
        except Exception as e:
            return Response(status=500, text=str(e))

    async def contact_info_by_id(self, request: Request) -> Response:
        try:
            contact_id = request.match_info.get('contact_id')
            contact: Contact = self._contact_service.get_contact_by_id(contact_id)

            return json_response(status=200, data=contact.to_dict())
        
        except Exception as e:
            return Response(status=500, text=str(e))