from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from person.models import Person
from person.schema import PersonIn, PersonOut

router = Router()


@router.post("/", url_name="person_create")
def create_person(request, payload: PersonIn):
    person = Person.objects.create(**payload.dict())
    return {"id": person.id}


@router.get("/{person_id}", response=PersonOut, url_name="person_get")
def get_person(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    return person


@router.get("/", response=List[PersonOut], url_name="person_list")
def list_persons(request):
    qs = Person.objects.all()
    return qs


@router.put("/{person_id}", url_name="person_edit")
def update_person(request, person_id: int, payload: PersonIn):
    person = get_object_or_404(Person, id=person_id)
    for attr, value in payload.dict().items():
        setattr(person, attr, value)
    person.save()
    return {"success": True}


@router.delete("/{person_id}", url_name="person_delete")
def delete_person(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return {"success": True}
