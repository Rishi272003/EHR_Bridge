from pydantic import BaseModel, model_validator , Field
from typing import List, Optional, Union
from datetime import datetime

class MetaData(BaseModel):
    lastUpdated: Optional[datetime] = None
    profile: Optional[Union[str, List[str]]] = None

class Coding(BaseModel):
    system: str
    code: str
    display: Optional[str] = None

class CodeableConcept(BaseModel):
    coding: Optional[List[Coding]] = None
    text: Optional[str] = None

    @model_validator(mode="after")
    def validate_content(self):
        if not self.coding and not self.text:
            raise ValueError("CodeableConcept must have coding or text")
        return self

class Patient(BaseModel):
    reference: str
    type: Optional[str] = None
    display: Optional[str] = None


class Manifestation(BaseModel):
    text: Optional[str] = None


class Reaction(BaseModel):
    manifestation: List[Manifestation]


class Request(BaseModel):
    method: str
    url: str

class MedicationCodeableConcept(BaseModel):
    coding: List[Coding]
    text: str

class DosageInstruction(BaseModel):
    text: Optional[str] = None

class Note(BaseModel):
    text: str

class Period(BaseModel):
    start: Optional[datetime] = None
    end: Optional[datetime] = None

class Attachment(BaseModel):
    contentType: str
    data: str
    hash: Optional[str] = None
    language: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None

class Content(BaseModel):
    attachment: Attachment

class Individuals(BaseModel):
    reference: str
    type: Optional[str] = None

class Participant(BaseModel):
    individual: Individuals
    period: Optional[Period] = None
    type: Optional[List[CodeableConcept]] = None


class Location(BaseModel):
    reference: str
    type: Optional[str] = None

class Locations(BaseModel):
    location: Location

class MedicationResource(BaseModel):
    resourceType: str
    meta: Optional[MetaData] = None
    status: Optional[str] = None
    intent: str
    medicationCodeableConcept: MedicationCodeableConcept
    subject: Optional[Patient] = None
    authoredOn: Optional[datetime] = None
    requester: Patient
    dosageInstruction: List[DosageInstruction]
    request: Request

class AllergyResource(BaseModel):
    resourceType: str
    id: Optional[str] = None
    meta: Optional[MetaData] = None
    clinicalStatus: Optional[CodeableConcept] = None
    verificationStatus: Optional[CodeableConcept] = None
    category: Optional[List[str]] = None
    criticality: Optional[str] = None
    code: CodeableConcept
    patient: Patient
    onsetDateTime: Optional[datetime] = None
    reaction: Optional[List[Reaction]] = None
    request: Request

class Conditons(BaseModel):
    resourceType: str = Field(default="Condition")
    id: Optional[str] = None
    meta: Optional[MetaData] = None
    clinicalStatus: Optional[CodeableConcept] = None
    verificationStatus: Optional[CodeableConcept] = None
    category: Optional[List[CodeableConcept]] = None
    severity: Optional[CodeableConcept] = None
    code: CodeableConcept
    subject: Patient
    onsetDateTime: Optional[datetime] = None
    abatementDateTime: Optional[datetime] = None
    recorder: Patient
    note: Optional[List[Note]] = None

class DocumentReference(BaseModel):
    resourceType: str = Field(default="DocumentReference")
    id: Optional[str] = None
    meta: Optional[MetaData] = None
    status: Optional[str] = None
    type: CodeableConcept
    category: Optional[List[CodeableConcept]] = None
    subject: Optional[Patient] = None
    date: Optional[datetime] = None
    author: Optional[List[Patient]] = None
    content: Optional[List[Content]] = None

class Encounter(BaseModel):
    resourceType: str = Field(default="Encounter")
    id: Optional[str] = None
    meta: Optional[MetaData] = None
    status: Optional[str] = None
    class_: Coding = Field(alias="class")
    type: List[CodeableConcept]
    subject: Patient
    participant: Optional[List[Participant]] = None
    period: Optional[Period] = None
    reasonCode: Optional[List[CodeableConcept]] = None
    location: Optional[List[Locations]] = None

class Entry(BaseModel):
    resource: Union[AllergyResource, MedicationResource, Conditons, Encounter, DocumentReference]
    request: Request

class FHIRBundle(BaseModel):
    resourceType: str
    id: Optional[str] = None
    meta: Optional[MetaData] = None
    type: str
    entry: List[Entry]

    def model_dump(self):
        return self.model_dump_json(mode="json", exclude_none=True)
