import axios from 'axios';


export interface PaginatedResponse<E> {
    count: number,
    next: string,
    previous:string,
    results: E[];
}

export interface AcousticFiles {
    id: number,
    recording_time: string;
    recording_location: string | null;
    file_name: string | null;
    s3_verified: boolean | null;
    length_ms: number | null;
    size_bytes: number | null;
    survey_event: null;
}

export interface Species {
    species_code: string;
    family: string;
    genus: string;
    common_name: string;
    species_code_6?: string;
}

export interface SpeciesBatch {
    species: string,

}

export interface SpectrogramAnnotation {
    offset: number,
    frequency: number,
}

export interface SpectrogramBatches {
    vetter: string | null;
    auto?: Species;
    manual?: Species;
}

export interface Spectrogram {
    url: string;
    filename: string;
    project: number;
    annotations?: SpectrogramAnnotation[];
    batches?: SpectrogramBatches[];
    images: string[];

}


export const axiosInstance = axios.create({
  baseURL: import.meta.env.VUE_APP_API_ROOT as string,
});


async function getAcousticFiles(offset=0, limit=-1) {
  const data = (await axiosInstance.get<PaginatedResponse<AcousticFiles>>(`/acoustic_file?offset=${offset}&limit=${limit}`)).data;
  return data;
}

async function getAcoustFilesS3Exists(offset=0, limit=-1) {
    const data = (await axiosInstance.get<PaginatedResponse<AcousticFiles>>(`/acoustic_file/s3_exists?offset=${offset}&limit=${limit}`)).data;
    return data;
  
}

async function getSpecies(offset=0, limit=-1) {
    const data = (await axiosInstance.get<PaginatedResponse<Species>>(`/species/?offset=${offset}&limit=${limit}`)).data;
    return data;

}

async function getSpectrogram(id: string, offset=0, limit=-1) {
    const data = (await axiosInstance.get<Spectrogram>(`/spectrogram/${id}?offset=${offset}&limit=${limit}`)).data;
    return data;

}


export {
 getAcousticFiles,
 getAcoustFilesS3Exists,
 getSpecies,
 getSpectrogram
};