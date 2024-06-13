from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from person.models import Person
from person.schema import PersonIn, PersonOut

router = Router()


@router.post("/")
def create_employee(request, payload: PersonIn):
    person = Person.objects.create(**payload.dict())
    return {"id": person.id}


@router.get("/{person_id}", response=PersonOut)
def get_person(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    return person


@router.get("/", response=List[PersonOut])
def list_persons(request):
    qs = Person.objects.all()
    return qs


@router.put("/{person_id}")
def update_employee(request, person_id: int, payload: PersonIn):
    person = get_object_or_404(Person, id=person_id)
    for attr, value in payload.dict().items():
        setattr(person, attr, value)
    person.save()
    return {"success": True}


@router.delete("/{person_id}")
def delete_employee(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return {"success": True}
