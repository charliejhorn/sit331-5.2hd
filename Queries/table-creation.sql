-- Region
CREATE TABLE region (
    id INT NOT NULL GENERATED ALWAYS AS IDENTITY
    Name TEXT NOT NULL
);

-- Aboriginal Tribe
CREATE TABLE aboriginaltribe (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Region INTEGER,
    FOREIGN KEY (Region) REFERENCES Region(ID)
);

-- Artist
CREATE TABLE Artist (
    ID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    RegionKey INTEGER,
    AboriginalTribeKey INTEGER,
    FOREIGN KEY (RegionKey) REFERENCES Region(ID),
    FOREIGN KEY (AboriginalTribeKey) REFERENCES AboriginalTribe(ID)
);

-- Artifact Type
CREATE TABLE ArtifactType (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Description TEXT
);

-- Artifact
CREATE TABLE Artifact (
    ID INTEGER PRIMARY KEY,
    Title TEXT NOT NULL,
    Description TEXT,
    Date TEXT,
    Image TEXT,
    ArtType TEXT,
    ArtEra TEXT,
    ArtifactTypeID INTEGER,
    FOREIGN KEY (ArtifactTypeID) REFERENCES ArtifactType(ID)
);

-- ArtistArtifactJoin (Many-to-Many)
CREATE TABLE ArtistArtifactJoin (
    ArtistKey INTEGER,
    ArtifactKey INTEGER,
    PRIMARY KEY (ArtistKey, ArtifactKey),
    FOREIGN KEY (ArtistKey) REFERENCES Artist(ID),
    FOREIGN KEY (ArtifactKey) REFERENCES Artifact(ID)
);

-- Image
CREATE TABLE Image (
    ID INTEGER PRIMARY KEY,
    Height INTEGER,
    Width INTEGER,
    SourceURL TEXT,
    Rights TEXT,
    ArtifactKey INTEGER,
    FOREIGN KEY (ArtifactKey) REFERENCES Artifact(ID)
);

-- Exhibition
CREATE TABLE Exhibition (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Description TEXT,
    StartDate TEXT,
    EndDate TEXT,
    Location TEXT,
    Gallery TEXT
);

-- ArtifactExhibitionJoin (Many-to-Many)
CREATE TABLE ArtifactExhibitionJoin (
    ArtifactKey INTEGER,
    ExhibitionKey INTEGER,
    PRIMARY KEY (ArtifactKey, ExhibitionKey),
    FOREIGN KEY (ArtifactKey) REFERENCES Artifact(ID),
    FOREIGN KEY (ExhibitionKey) REFERENCES Exhibition(ID)
);

-- User
CREATE TABLE User (
    ID INTEGER PRIMARY KEY,
    FirstName TEXT NOT NULL,
    LastName TEXT NOT NULL,
    Roles INTEGER,
    Username TEXT UNIQUE,
    Email TEXT,
    Password TEXT,
    MembershipType TEXT,
    FOREIGN KEY (Roles) REFERENCES Role(ID)
);

-- Role
CREATE TABLE Role (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL
);

-- Comment (with parent-child relationship)
CREATE TABLE Comment (
    ID INTEGER PRIMARY KEY,
    User INTEGER,
    ArtifactKey INTEGER,
    ParentCommentKey INTEGER,
    Date TEXT,
    FOREIGN KEY (User) REFERENCES User(ID),
    FOREIGN KEY (ArtifactKey) REFERENCES Artifact(ID),
    FOREIGN KEY (ParentCommentKey) REFERENCES Comment(ID)
);
