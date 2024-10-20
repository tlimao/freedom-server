import logging
from typing import List
from aiohttp import web

from freedomlib.contact.contact import Contact

from freedomserver.context.contact.contact_service import ContactService
from freedomserver.context.contact.dtos.fetch_contacts_request import FetchContactsRequest
from freedomserver.context.contact.dtos.fetch_contacts_response import FetchContactsResponse
from freedomserver.context.contact.errors.contact_error import ContactNotFoundError


class ContactController:
    
    def __init__(self, contact_service: ContactService) -> None:
        self._contact_service: ContactService = contact_service

    async def fetch_contacts(self, request: web.Request) -> web.Response:
        try:
            fetch_contact_request: FetchContactsRequest = FetchContactsRequest.from_dict(await request.json())
            
            contacts: List[Contact] = self._contact_service.get_contacts(fetch_contact_request.phonenumbers)
            
            fetch_contact_response: FetchContactsResponse = FetchContactsResponse(contacts)
            
            return web.json_response(fetch_contact_response.to_dict())
            
        except ContactNotFoundError as e:
            logging.error(e)
            return web.Response(status=500, body=str(e))
            